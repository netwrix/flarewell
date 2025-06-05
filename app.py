#!/usr/bin/env python3
"""
HTML to Markdown Documentation Converter
Converts HTML documentation (from MadCap Flare) to Markdown format
while preserving folder structure and centralizing images.
"""

import os
import shutil
from pathlib import Path
import re
import argparse
from urllib.parse import unquote, urlparse
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import hashlib
import json
from collections import defaultdict


class HTMLToMarkdownConverter:
    def __init__(self, input_dir, output_dir, verbose=False, flatten_dirs=False, docusaurus=False, lowercase_filenames=False):
        self.input_dir = Path(input_dir).resolve()  # Always use absolute paths
        self.output_dir = Path(output_dir).resolve()  # Always use absolute paths
        # Place static directory at the same level as output directory
        self.images_dir = self.output_dir.parent / 'static' / 'img'
        self.verbose = verbose
        self.flatten_dirs = flatten_dirs
        self.docusaurus = docusaurus
        self.lowercase_filenames = lowercase_filenames
        self.image_counter = 0
        self.image_mappings = {}
        self.referenced_images = set()  # Track all referenced images
        self.flattened_paths = {}  # Cache for flattened paths
        self.doc_image_mapping = {}  # Track which doc references which images
        self.image_hash_map = {}  # Map file hash to destination path
        self.image_manifest = defaultdict(lambda: {
            'original_paths': set(),
            'used_by': set(),
            'destination': None,
            'hash': None
        })  # Comprehensive image tracking
        
    def log(self, message):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(message)
            
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file content"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def extract_topic_and_section(self, html_file, image_path):
        """Extract product/topic and major section from file path"""
        # Get relative path from input directory
        try:
            rel_path = html_file.relative_to(self.input_dir)
        except ValueError:
            rel_path = html_file
            
        parts = list(rel_path.parts[:-1])  # Exclude the filename
        
        # Determine product/topic (first level)
        product = parts[0].lower() if parts else 'general'
        
        # Determine section (second level, if exists)
        section = None
        if len(parts) > 1:
            # Try to identify major sections
            second_level = parts[1].lower()
            
            # Common documentation sections
            major_sections = {
                'admin', 'administration', 'config', 'configuration',
                'install', 'installation', 'guide', 'guides', 'tutorial',
                'api', 'reference', 'security', 'integration', 'troubleshooting',
                'overview', 'requirements', 'tools', 'reports', 'dashboard'
            }
            
            if second_level in major_sections:
                section = second_level
            elif len(parts) > 2:
                # Check third level too
                third_level = parts[2].lower()
                if third_level in major_sections:
                    section = third_level
                else:
                    # Use second level as section
                    section = second_level
            else:
                section = second_level
                
        # Check if this appears to be a shared/common image
        image_name_lower = image_path.name.lower()
        shared_indicators = ['logo', 'icon', 'banner', 'header', 'footer', 'common', 'shared']
        if any(indicator in image_name_lower for indicator in shared_indicators):
            return 'shared', None
            
        return product, section
    
    def lowercase_path(self, path):
        """Convert path to lowercase for Docusaurus compatibility"""
        if not self.lowercase_filenames:
            return path
        
        # Convert each part of the path to lowercase
        parts = list(path.parts)
        # Keep the file extension case as-is, but lowercase the filename
        if len(parts) > 0:
            # Handle the filename specially
            filename = parts[-1]
            if '.' in filename:
                name, ext = filename.rsplit('.', 1)
                parts[-1] = name.lower() + '.' + ext
            else:
                parts[-1] = filename.lower()
            
            # Lowercase all directory names
            for i in range(len(parts) - 1):
                parts[i] = parts[i].lower()
        
        return Path(*parts) if parts else path
            
    def flatten_path(self, path):
        """Remove redundant nested directories from a path"""
        if not self.flatten_dirs:
            return path
            
        # Check cache first
        path_str = str(path)
        if path_str in self.flattened_paths:
            return self.flattened_paths[path_str]
            
        parts = path.parts
        new_parts = []
        
        for i, part in enumerate(parts):
            # Check if this part is the same as the previous part
            if i == 0 or part != parts[i-1]:
                new_parts.append(part)
            else:
                self.log(f"  → Flattening redundant directory: {part}/{part}")
                
        result = Path(*new_parts) if new_parts else path
        self.flattened_paths[path_str] = result
        return result
            
    def find_image_references(self, image_name):
        """Find all HTML files that reference a specific image"""
        print(f"\nSearching for references to: {image_name}")
        
        # Find all HTML files
        html_files = []
        extensions = ['*.html', '*.HTML', '*.htm', '*.HTM', '*.xhtml', '*.XHTML']
        for ext in extensions:
            html_files.extend(self.input_dir.rglob(ext))
        html_files = sorted(list(set(html_files)))
        
        references = []
        image_paths_found = set()
        
        # Search each HTML file
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, 'html.parser')
                
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if not src:
                        continue
                    
                    # Check if this image matches the search
                    src_filename = Path(unquote(src)).name
                    if image_name.lower() in src_filename.lower():
                        # Calculate full path
                        if not src.startswith('http'):
                            src_path = Path(html_file).parent / unquote(src)
                            src_path = src_path.resolve()
                            image_paths_found.add(str(src_path))
                        else:
                            src_path = src
                        
                        # Get line number
                        line_num = html_content[:html_content.find(str(img))].count('\n') + 1
                        
                        references.append({
                            'html_file': html_file,
                            'line': line_num,
                            'src_attr': src,
                            'full_path': src_path,
                            'img_tag': str(img)[:100] + '...' if len(str(img)) > 100 else str(img)
                        })
                        
            except Exception as e:
                print(f"Error reading {html_file}: {str(e)}")
        
        # Display results
        if references:
            print(f"\nFound {len(references)} reference(s) to images matching '{image_name}':")
            
            # Group by HTML file
            from itertools import groupby
            references.sort(key=lambda x: x['html_file'])
            
            for html_file, refs in groupby(references, key=lambda x: x['html_file']):
                refs_list = list(refs)
                print(f"\n📄 {html_file.relative_to(self.input_dir)}")
                for ref in refs_list:
                    print(f"   Line {ref['line']}: src=\"{ref['src_attr']}\"")
                    if self.verbose:
                        print(f"   Tag: {ref['img_tag']}")
            
            # Show unique image paths found
            print(f"\nUnique image paths found: {len(image_paths_found)}")
            for path in sorted(image_paths_found):
                try:
                    rel_path = Path(path).relative_to(self.input_dir)
                    exists = "✓" if Path(path).exists() else "✗"
                    print(f"  {exists} {rel_path}")
                except:
                    exists = "✓" if Path(path).exists() else "✗"
                    print(f"  {exists} {path}")
        else:
            print(f"\nNo references found to images matching '{image_name}'")
            
            # Suggest similar image names
            all_images = []
            image_extensions = ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', 
                              '*.gif', '*.GIF', '*.bmp', '*.BMP', '*.svg', '*.SVG']
            for ext in image_extensions:
                all_images.extend(self.input_dir.rglob(ext))
            
            similar_images = [img for img in all_images if image_name.lower() in img.name.lower()]
            if similar_images:
                print(f"\nDid you mean one of these images?")
                for img in similar_images[:10]:
                    print(f"  - {img.name}")
    
    def convert(self):
        """Main conversion process"""
        print(f"Converting HTML documentation from: {self.input_dir}")
        print(f"Output directory: {self.output_dir}")
        if self.flatten_dirs:
            print("Directory flattening: ENABLED (removing redundant nested directories)")
        if self.docusaurus:
            print("Docusaurus mode: ENABLED (adding frontmatter and cleaning navigation)")
        
        # Create output directories (unless dry run)
        if not hasattr(self, 'dry_run') or not self.dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all HTML files (case-insensitive, multiple extensions)
        html_files = []
        extensions = ['*.html', '*.HTML', '*.htm', '*.HTM', '*.xhtml', '*.XHTML']
        for ext in extensions:
            html_files.extend(self.input_dir.rglob(ext))
        
        # Remove duplicates and sort
        html_files = sorted(list(set(html_files)))
        print(f"Found {len(html_files)} HTML files to convert")
        
        # List file extensions found
        found_extensions = set(f.suffix.lower() for f in html_files)
        print(f"File types found: {', '.join(found_extensions)}")
        
        # First pass: scan all HTML files to find referenced images and build anchor mappings
        print("\nFirst pass: Scanning for referenced images and building anchor mappings...")
        self.global_anchor_mappings = {}  # Maps file -> anchor -> heading text
        self.global_truncated_mappings = {}  # Maps truncated anchor -> [(file, heading_text), ...]
        
        for html_file in html_files:
            self.scan_for_images(html_file)
            self.build_anchor_mappings(html_file)
        
        print(f"Found {len(self.referenced_images)} referenced images")
        print(f"Built anchor mappings for {len(self.global_anchor_mappings)} files")
        
        # Find all image files in the input directory
        all_images = []
        image_extensions = ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', 
                          '*.gif', '*.GIF', '*.bmp', '*.BMP', '*.svg', '*.SVG',
                          '*.webp', '*.WEBP', '*.ico', '*.ICO']
        for ext in image_extensions:
            all_images.extend(self.input_dir.rglob(ext))
        
        unreferenced_images = [img for img in all_images if str(img.resolve()) not in self.referenced_images]
        print(f"Found {len(unreferenced_images)} unreferenced images (will not be copied)")
        
        if self.verbose and unreferenced_images:
            print("\nUnreferenced images:")
            for img in unreferenced_images[:10]:
                print(f"  - {img.relative_to(self.input_dir)}")
            if len(unreferenced_images) > 10:
                print(f"  ... and {len(unreferenced_images) - 10} more")
        
        # Second pass: process and convert HTML files
        print("\nConverting HTML files...")
        for i, html_file in enumerate(html_files, 1):
            self.log(f"\n[{i}/{len(html_files)}] Processing: {html_file.relative_to(self.input_dir)}")
            self.process_html_file(html_file)
            
        # Save image manifest
        self.save_image_manifest()
        
        print(f"\nConversion complete!")
        print(f"- Converted {len(html_files)} HTML files")
        print(f"- Copied {self.image_counter} referenced images to static/img/")
        print(f"- Skipped {len(unreferenced_images)} unreferenced images")
        
        # Show deduplication stats
        total_refs = sum(len(info['used_by']) for info in self.image_manifest.values())
        if total_refs > self.image_counter and self.image_counter > 0:
            saved = total_refs - self.image_counter
            print(f"- Deduplication saved {saved} file copies ({saved/total_refs*100:.1f}% reduction)")
    
    def save_image_manifest(self):
        """Save image manifest to JSON file"""
        manifest_path = self.images_dir / 'image-manifest.json'
        
        # Convert sets to lists for JSON serialization
        manifest_data = {}
        for image_name, info in self.image_manifest.items():
            manifest_data[image_name] = {
                'hash': info['hash'],
                'destination': info['destination'],
                'original_paths': list(info['original_paths']),
                'used_by': list(info['used_by']),
                'reference_count': len(info['used_by'])
            }
        
        # Sort by reference count (most used first)
        sorted_manifest = dict(sorted(
            manifest_data.items(), 
            key=lambda x: x[1]['reference_count'], 
            reverse=True
        ))
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_manifest, f, indent=2, ensure_ascii=False)
        
        self.log(f"  ✓ Saved image manifest: {manifest_path}")
        
    def scan_for_images(self, html_file):
        """Scan HTML file for referenced images without processing"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Scan anchor tags that link to images
            for link in soup.find_all('a'):
                href = link.get('href')
                if not href or href.startswith('http'):
                    continue
                    
                # Check if this is an image link
                if any(href.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']):
                    src_path = Path(html_file).parent / unquote(href)
                    src_path = src_path.resolve()
                    
                    if src_path.exists():
                        self.referenced_images.add(str(src_path))
            
            # Scan img tags
            for img in soup.find_all('img'):
                src = img.get('src')
                if not src or src.startswith('http'):
                    continue
                
                # Calculate source image path
                src_path = Path(html_file).parent / unquote(src)
                src_path = src_path.resolve()
                
                if src_path.exists():
                    self.referenced_images.add(str(src_path))
                    
        except Exception as e:
            self.log(f"  ✗ Error scanning {html_file}: {str(e)}")
    
    def build_anchor_mappings(self, html_file):
        """Build global anchor mappings for cross-file reference resolution"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Get relative path for the output file
            rel_path = html_file.relative_to(self.input_dir)
            if self.flatten_dirs:
                rel_path = self.flatten_path(rel_path)
            if self.lowercase_filenames:
                rel_path = self.lowercase_path(rel_path)
            
            # Convert to markdown extension
            output_path = rel_path.with_suffix('.md')
            file_key = str(output_path).replace('\\', '/')
            
            # Initialize mappings for this file
            self.global_anchor_mappings[file_key] = {}
            
            # Process headings to find anchors
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                # Check for anchor IDs
                anchor_id = heading.get('name') or heading.get('id')
                
                # Check for anchor tags within the heading
                anchor = heading.find('a', {'name': True})
                if anchor and not anchor_id:
                    anchor_id = anchor.get('name')
                
                # Check for anchor before heading
                if not anchor_id:
                    prev_sibling = heading.find_previous_sibling()
                    if prev_sibling and prev_sibling.name == 'a' and prev_sibling.get('name'):
                        anchor_id = prev_sibling.get('name')
                
                heading_text = heading.get_text(strip=True)
                if not heading_text:
                    continue
                
                if anchor_id:
                    # Store the mapping
                    self.global_anchor_mappings[file_key][anchor_id] = heading_text
                    
                    # Generate the Docusaurus ID for this heading
                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                    self.global_anchor_mappings[file_key][anchor_id + '_docusaurus'] = docusaurus_id
                    
                    # Also store truncated versions if applicable
                    if len(anchor_id) <= 8 and not '-' in anchor_id:
                        # This is likely already truncated
                        if anchor_id not in self.global_truncated_mappings:
                            self.global_truncated_mappings[anchor_id] = []
                        self.global_truncated_mappings[anchor_id].append((file_key, heading_text))
                    elif len(anchor_id) > 8:
                        # Store potential truncated version
                        truncated = anchor_id[:8]
                        if truncated not in self.global_truncated_mappings:
                            self.global_truncated_mappings[truncated] = []
                        self.global_truncated_mappings[truncated].append((file_key, heading_text))
                else:
                    # For headings without explicit anchors, Docusaurus will generate from text
                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                    # Try to guess potential MadCap anchor patterns
                    if heading.name == 'h1':
                        # MadCap might use heading text with underscores
                        implicit_anchor = heading_text.replace(' ', '_')
                        self.global_anchor_mappings[file_key][implicit_anchor] = heading_text
                        self.global_anchor_mappings[file_key][implicit_anchor + '_docusaurus'] = docusaurus_id
                
        except Exception as e:
            self.log(f"  ✗ Error building anchor mappings for {html_file}: {str(e)}")
    
    def process_html_file(self, html_file):
        """Process a single HTML file"""
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Debug: Check pre tags before any processing
            if self.verbose:
                pre_tags_before = soup.find_all('pre')
                if pre_tags_before:
                    self.log(f"  → Found {len(pre_tags_before)} pre tags before processing")
                    for idx, pre in enumerate(pre_tags_before):
                        content = pre.get_text()[:50] + '...' if len(pre.get_text()) > 50 else pre.get_text()
                        self.log(f"    Pre tag {idx + 1} before: {repr(content)}")
            
            # Process images before conversion
            self.process_images(soup, html_file)
            
            # Remove MadCap Flare specific elements
            self.clean_madcap_elements(soup)
            
            # Pre-process code tags to preserve their content without escaping
            # Convert <code> tags to temporary markers to handle them specially
            code_blocks = []
            for code_tag in soup.find_all('code'):
                # Get the raw text content without any escaping
                code_content = code_tag.get_text()
                # Store the content
                code_blocks.append(code_content)
                # Replace with a temporary marker
                marker = f"CODE_BLOCK_{len(code_blocks) - 1}_MARKER"
                code_tag.string = marker
            
            # Debug: Check pre tags after clean_madcap_elements
            if self.verbose:
                pre_tags_after = soup.find_all('pre')
                if pre_tags_after:
                    self.log(f"  → Found {len(pre_tags_after)} pre tags after clean_madcap_elements")
                    for idx, pre in enumerate(pre_tags_after):
                        content = pre.get_text()[:50] + '...' if len(pre.get_text()) > 50 else pre.get_text()
                        self.log(f"    Pre tag {idx + 1} after clean: {repr(content)}")
            
            # First preserve heading IDs before conversion
            # This must come BEFORE process_document_links so that anchor mappings are available
            self.preserve_heading_ids(soup)
            
            # Process document links after preserve_heading_ids so we have anchor mappings
            self.process_document_links(soup, html_file)
            
            # Debug: Log soup right before conversion
            if self.verbose and soup.find_all('pre'):
                self.log(f"  → Soup right before markdownify conversion:")
                for pre in soup.find_all('pre'):
                    self.log(f"    Pre content: {repr(pre.get_text()[:100])}")
            
            # Remove script and style tags before conversion
            # This ensures their content is completely removed
            for script in soup.find_all('script'):
                script.decompose()
            for style in soup.find_all('style'):
                style.decompose()
            
            # Convert to markdown with better HTML handling
            markdown_content = md(
                str(soup),
                heading_style="ATX",
                bullets="-",
                code_language="",
                autolinks=False,
                strip=['script', 'style', 'meta', 'link', 'noscript']  # Remove these tags entirely
            )
            
            # Restore code blocks with triple backticks and no escaping
            for i, code_content in enumerate(code_blocks):
                marker = f"CODE_BLOCK_{i}_MARKER"
                # Replace the marker with triple backtick code blocks
                # The content is preserved exactly as it was in the HTML
                markdown_content = markdown_content.replace(f"`{marker}`", f"```{code_content}```")
                # Also handle cases where markdownify might have processed it differently
                markdown_content = markdown_content.replace(marker, f"```{code_content}```")
            
            # Debug: Check for /* */ right after conversion
            if '/\\*' in markdown_content and '\\*/' in markdown_content:
                self.log(f"  ⚠ Found /* */ pattern in markdown")
            
            # Debug: Check code blocks in markdown
            if self.verbose and '```' in markdown_content:
                self.log(f"  → Found code blocks in markdown")
                # Extract code blocks
                code_blocks = re.findall(r'```[^\n]*\n(.*?)\n```', markdown_content, re.DOTALL)
                for idx, block in enumerate(code_blocks):
                    content = block[:50] + '...' if len(block) > 50 else block
                    self.log(f"    Code block {idx + 1}: {repr(content)}")
            
            # Clean up the markdown
            markdown_content = self.clean_markdown(markdown_content)
            
            # Debug: Check code blocks after clean_markdown
            if self.verbose and '```' in markdown_content:
                self.log(f"  → After clean_markdown, checking code blocks")
                code_blocks = re.findall(r'```[^\n]*\n(.*?)\n```', markdown_content, re.DOTALL)
                for idx, block in enumerate(code_blocks):
                    content = block[:50] + '...' if len(block) > 50 else block
                    self.log(f"    Code block {idx + 1} after clean: {repr(content)}")
            
            # Restore anchors - always do this to preserve heading IDs
            markdown_content = self.restore_heading_anchors(markdown_content)
            
            # Add Docusaurus frontmatter if enabled
            if self.docusaurus:
                markdown_content = self.add_docusaurus_frontmatter(markdown_content, html_file)
                # Restore anchors in MDX-compatible format (for standalone anchors)
                markdown_content = self.restore_mdx_anchors(markdown_content)
                # Final MDX cleanup specifically for Docusaurus
                markdown_content = self.final_mdx_cleanup(markdown_content)
            
            # Calculate output path
            relative_path = html_file.relative_to(self.input_dir)
            # Apply flattening if enabled
            flattened_path = self.flatten_path(relative_path)
            # Apply lowercase conversion if enabled (for Docusaurus)
            final_path = self.lowercase_path(flattened_path)
            markdown_path = self.output_dir / final_path.with_suffix('.md')
            
            # Create parent directories
            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            
            # FINAL FIX: Escape any remaining pipes in table cells right before writing
            # This is our last chance to fix stubborn patterns
            lines = markdown_content.split('\n')
            
            # First pass: Find tables and fix column consistency
            table_column_count = None
            in_table = False
            table_start = -1
            
            for i, line in enumerate(lines):
                # Detect table start
                if '|' in line and line.count('|') >= 2:
                    if not in_table:
                        # Check if next line is separator
                        if i + 1 < len(lines) and re.match(r'^[\s\-|:]+$', lines[i + 1]):
                            in_table = True
                            table_start = i
                            # Count columns from header
                            table_column_count = line.count('|') - 1  # Subtract 1 for leading/trailing pipes
                    
                    if in_table and table_column_count:
                        # Fix column count for this row
                        current_columns = line.count('|') - 1
                        if current_columns < table_column_count:
                            # Add empty columns
                            missing_columns = table_column_count - current_columns
                            # Remove trailing pipe if exists
                            if line.rstrip().endswith('|'):
                                line = line.rstrip()[:-1]
                            # Add missing columns
                            line = line + ' |' * missing_columns + ' |'
                            lines[i] = line
                        elif current_columns > table_column_count:
                            # Too many columns - this might be a new table or error
                            # For now, leave it as is
                            pass
                
                # Detect table end
                elif in_table and line.strip() == '':
                    in_table = False
                    table_column_count = None
            
            # Second pass: Apply all other fixes
            for i, line in enumerate(lines):
                # POLICYPAK FIXES: Apply to all lines, not just tables
                # Fix 1: Remove curly braces from GUIDs (common in PolicyPak)
                # Pattern: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
                if '{' in line and '}' in line:
                    # Don't process if it's already in a code block
                    if not line.strip().startswith('`'):
                        # Remove braces from GUID patterns
                        line = re.sub(r'\{([A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\}', 
                                     r'\1', line, flags=re.IGNORECASE)
                        # For any other curly braces (like placeholders), escape them
                        line = re.sub(r'(?<!\\)\{([^}]+)\}', r'\\{\1\\}', line)
                
                # Fix 2: Handle percent variables (common in PolicyPak paths)
                # Pattern: %ProgramData%, %LOCALAPPDATA%, etc.
                if '%' in line:
                    line = re.sub(r'(?<!`)%([A-Za-z0-9_]+)%(?!`)', r'`%\1%`', line)
                
                # Fix 3: Escape square brackets in URLs and parameters
                # Pattern: [dl=0], [dl=1], etc.
                if '[' in line and ']' in line:
                    # Don't escape if in code block or if it's a markdown link
                    if not line.strip().startswith('`') and not re.search(r'\]\([^)]+\)', line):
                        # Escape square brackets that look like parameters
                        line = re.sub(r'\[([^]]+=[^]]+)\]', r'\\[\1\\]', line)
                        # Also escape other square brackets that might cause issues
                        line = re.sub(r'(?<!\\)\[([^]]+)\]', r'\\[\1\\]', line)
                
                # Fix 4: Wrap inline XML/HTML tags in backticks
                # Pattern: <tag attr=value or </tag> in regular text
                if '<' in line and not line.strip().startswith('`'):
                    # Don't process if it's a full HTML line or in a code block
                    if not line.strip().startswith('<') and not line.strip().startswith('```'):
                        # Find and wrap XML/HTML tags that aren't already wrapped
                        line = re.sub(r'(?<!`)"<([^>"]+)"', r'"`<\1>`"', line)  # Quoted tags
                        line = re.sub(r'(?<!`)(<[^>]+>)(?!`)', r'`\1`', line)   # Unquoted tags
                
                # If this is a table row (has 3+ pipes)
                if '|' in line and line.count('|') >= 3:
                    # Escape any letter|letter patterns
                    line = re.sub(r'([a-zA-Z])\|([a-zA-Z])', r'\1\\|\2', line)
                    
                    # Fix triple backticks within table cells
                    # Replace ``` with ` at the start and end of code blocks in cells
                    # First, handle cases where triple backticks are at the end of a cell
                    line = re.sub(r'```\s*\|', '` |', line)
                    # Then handle cases where triple backticks start a code block
                    line = re.sub(r'\|\s*```', '| `', line)
                    # Handle any remaining triple backticks within cells
                    parts = line.split('|')
                    for j, part in enumerate(parts):
                        if '```' in part:
                            # Replace starting triple backticks
                            part = re.sub(r'(^|\s)```(\S)', r'\1`\2', part)
                            # Replace ending triple backticks
                            part = re.sub(r'(\S)```($|\s)', r'\1`\2', part)
                            # Replace any standalone triple backticks
                            part = part.replace('```', '`')
                        
                        # POLICYPAK: Additional fixes for table cells
                        # Remove curly braces from GUIDs in table cells
                        if '{' in part or '\\{' in part:
                            if not (part.strip().startswith('`') and part.strip().endswith('`')):
                                # First handle already escaped GUIDs (with \\{ and \\})
                                part = re.sub(r'\\\\\{([A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\\\\\}', 
                                            r'\1', part, flags=re.IGNORECASE)
                                # Then handle non-escaped GUIDs (with { and })
                                part = re.sub(r'\{([A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12})\}', 
                                            r'\1', part, flags=re.IGNORECASE)
                                # For any other curly braces that aren't GUIDs, escape them
                                # First check if there are any remaining unescaped braces
                                if re.search(r'(?<!\\)\{[^}]+\}', part) and not re.search(r'\{[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}\}', part, re.IGNORECASE):
                                    part = re.sub(r'(?<!\\)\{([^}]+)\}', r'\\{\1\\}', part)
                        
                        # Fix XML tags within table cells
                        # Look for patterns like </RelatedItem or <tag> that might cause issues
                        if '<' in part or '>' in part:
                            # First check if it's an unclosed tag at the end
                            # Pattern: text</tag with no closing >
                            if re.search(r'<[^>]+$', part):
                                # Add missing closing >
                                part = part + '>'
                            
                            # Wrap XML/HTML tags in backticks if not already wrapped
                            # But only if the entire cell isn't already in backticks
                            if not (part.strip().startswith('`') and part.strip().endswith('`')):
                                # Find all XML/HTML tags
                                part = re.sub(r'(<[^>]+>)', r'`\1`', part)
                        
                        parts[j] = part
                    line = '|'.join(parts)
                    
                lines[i] = line
            markdown_content = '\n'.join(lines)
            
            # Write markdown file
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                
            self.log(f"  ✓ Created: {markdown_path.relative_to(self.output_dir)}")
            
        except Exception as e:
            print(f"  ✗ Error processing {html_file}: {str(e)}")
            
    def process_images(self, soup, html_file):
        """Process all images in the HTML file"""
        # First, process anchor tags that link to images (like popup/lightbox images)
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
                
            # Check if this anchor links to an image
            if any(href.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']):
                # Skip external images
                if href.startswith('http'):
                    continue
                    
                # Calculate source image path
                src_path = Path(html_file).parent / unquote(href)
                src_path = src_path.resolve()
                
                if not src_path.exists():
                    self.log(f"  ⚠ Linked image not found: {href}")
                    continue
                
                # Only process images that were found in the scan phase
                if str(src_path) in self.referenced_images:
                    # Get the destination path from our mappings
                    if str(src_path) in self.image_mappings:
                        dest_path = self.image_mappings[str(src_path)]
                    else:
                        # Process this image if not already processed
                        image_hash = self.calculate_file_hash(src_path)
                        
                        if image_hash in self.image_hash_map:
                            dest_path = self.image_hash_map[image_hash]
                        else:
                            # New image, determine destination
                            product, section = self.extract_topic_and_section(html_file, src_path)
                            
                            if section:
                                dest_rel_path = Path(product) / section / src_path.name
                            else:
                                dest_rel_path = Path(product) / src_path.name
                            
                            dest_path = self.images_dir / dest_rel_path
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            # Handle conflicts
                            if dest_path.exists():
                                existing_hash = self.calculate_file_hash(dest_path)
                                if existing_hash != image_hash:
                                    base = dest_path.stem
                                    ext = dest_path.suffix
                                    counter = 1
                                    while dest_path.exists():
                                        dest_path = dest_path.parent / f"{base}_{counter}{ext}"
                                        counter += 1
                            
                            # Copy if needed
                            if not dest_path.exists():
                                shutil.copy2(src_path, dest_path)
                                self.image_counter += 1
                                self.log(f"  → Copied linked image: {dest_rel_path}")
                            
                            # Update tracking
                            self.image_hash_map[image_hash] = dest_path
                            self.image_mappings[str(src_path)] = dest_path
                            
                            # Update manifest
                            image_name = src_path.name
                            self.image_manifest[image_name]['hash'] = image_hash
                            self.image_manifest[image_name]['destination'] = str(dest_path.relative_to(self.images_dir))
                            self.image_manifest[image_name]['used_by'].add(str(html_file))
                            self.image_manifest[image_name]['original_paths'].add(str(src_path))
                    
                    # Update the link href
                    img_path = dest_path.relative_to(self.images_dir)
                    abs_path = '/static/img/' + str(img_path).replace('\\', '/')
                    link['href'] = abs_path
                    self.log(f"  → Updated image link: {href} → {abs_path}")
        
        # Then process regular img tags
        for img in soup.find_all('img'):
            src = img.get('src')
            if not src:
                continue
                
            # Calculate source image path
            if src.startswith('http'):
                self.log(f"  ⚠ Skipping external image: {src}")
                continue
                
            # Handle relative paths
            src_path = Path(html_file).parent / unquote(src)
            src_path = src_path.resolve()
            
            if not src_path.exists():
                self.log(f"  ⚠ Image not found: {src}")
                continue
            
            # Only process images that were found in the scan phase
            if str(src_path) not in self.referenced_images:
                self.log(f"  ⚠ Image not in referenced set: {src}")
                continue
                
            # Calculate image hash for deduplication
            image_hash = self.calculate_file_hash(src_path)
            
            # Check if we've already processed this image (by hash)
            if image_hash in self.image_hash_map:
                # Image already processed, reuse existing destination
                dest_path = self.image_hash_map[image_hash]
                self.log(f"  → Reusing existing image: {dest_path.relative_to(self.images_dir)}")
                
                # Update manifest tracking
                self.image_manifest[src_path.name]['used_by'].add(str(html_file))
                self.image_manifest[src_path.name]['original_paths'].add(str(src_path))
            else:
                # New image, determine destination using topic/section organization
                product, section = self.extract_topic_and_section(html_file, src_path)
                
                # Build destination path
                if section:
                    dest_rel_path = Path(product) / section / src_path.name
                else:
                    dest_rel_path = Path(product) / src_path.name
                
                # Create destination path
                dest_path = self.images_dir / dest_rel_path
                
                # Create parent directories if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Handle filename conflicts by appending number
                if dest_path.exists():
                    # Check if it's actually the same file
                    existing_hash = self.calculate_file_hash(dest_path)
                    if existing_hash == image_hash:
                        # Same content, different source path
                        self.log(f"  → Found duplicate image, reusing: {dest_rel_path}")
                    else:
                        # Different content, same name - need unique name
                        base = dest_path.stem
                        ext = dest_path.suffix
                        counter = 1
                        while dest_path.exists():
                            dest_path = dest_path.parent / f"{base}_{counter}{ext}"
                            counter += 1
                        self.log(f"  → Name conflict resolved: {dest_path.relative_to(self.images_dir)}")
                
                # Copy the image if it doesn't exist
                if not dest_path.exists():
                    shutil.copy2(src_path, dest_path)
                    self.image_counter += 1
                    self.log(f"  → Copied image: {dest_rel_path}")
                
                # Update tracking
                self.image_hash_map[image_hash] = dest_path
                self.image_mappings[str(src_path)] = dest_path
                
                # Update manifest
                image_name = src_path.name
                self.image_manifest[image_name]['hash'] = image_hash
                self.image_manifest[image_name]['destination'] = str(dest_path.relative_to(self.images_dir))
                self.image_manifest[image_name]['used_by'].add(str(html_file))
                self.image_manifest[image_name]['original_paths'].add(str(src_path))
                
            # Update image reference in HTML
            # Always use full absolute path including /static/
            img_path = dest_path.relative_to(self.images_dir)
            abs_path = '/img/' + str(img_path).replace('\\', '/')
            img['src'] = abs_path
            
    def process_document_links(self, soup, html_file):
        """Process all document links in the HTML file"""
        # Process <a> tags
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
                
            # Skip external links 
            if href.startswith(('http://', 'https://', 'mailto:')):
                continue
                
            # Handle internal anchors (starting with #)
            if href.startswith('#'):
                anchor = href[1:]  # Remove the #
                
                if self.docusaurus:
                    # For Docusaurus, convert to Docusaurus-style IDs
                    sanitized_anchor = anchor.replace(':', '_').replace('&', '_and_')
                    sanitized_anchor = sanitized_anchor.lstrip('_')
                    
                    # Check if this is a truncated MadCap anchor (8 characters or less)
                    is_truncated = len(anchor) <= 8 and not '-' in anchor
                    
                    # If we have a heading mapping for this anchor, use the heading text
                    docusaurus_id = None
                    
                    # First check if we have a direct mapping from the original anchor ID
                    if hasattr(self, 'original_anchor_mappings') and anchor in self.original_anchor_mappings:
                        heading_text = self.original_anchor_mappings[anchor]
                        docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                        self.log(f"  → Found original anchor mapping: {anchor} → {heading_text}")
                    
                    # Next check if this is a known truncated anchor
                    elif hasattr(self, 'truncated_anchor_mappings') and anchor in self.truncated_anchor_mappings:
                        heading_text = self.truncated_anchor_mappings[anchor]
                        docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                        self.log(f"  → Found truncated anchor mapping: {anchor} → {heading_text}")
                    
                    # Otherwise check regular mappings
                    elif hasattr(self, 'anchor_mappings'):
                        # First try exact match
                        for heading_text, anchor_id in self.anchor_mappings.items():
                            if anchor_id == sanitized_anchor:
                                docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                break
                        
                        # If no exact match and this looks like a truncated anchor,
                        # try to find a heading that starts with this truncated text
                        if not docusaurus_id and is_truncated:
                            for heading_text, anchor_id in self.anchor_mappings.items():
                                # Check if the anchor ID starts with the truncated version
                                if anchor_id.lower().startswith(anchor.lower()):
                                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                    self.log(f"  → Matched truncated anchor '{anchor}' to heading '{heading_text}'")
                                    break
                    
                    # Use the mapped ID or convert the anchor directly
                    if docusaurus_id:
                        link['href'] = '#' + docusaurus_id
                        self.log(f"  → Converted internal anchor to Docusaurus format: {href} → #{docusaurus_id}")
                    else:
                        docusaurus_id = self.madcap_to_docusaurus_id(sanitized_anchor)
                        link['href'] = '#' + docusaurus_id
                        self.log(f"  → Converted internal anchor to Docusaurus format: {href} → #{docusaurus_id}")
                else:
                    # Non-Docusaurus mode - just sanitize
                    sanitized_anchor = anchor.replace(':', '_').replace('&', '_and_')
                    sanitized_anchor = sanitized_anchor.lstrip('_')
                    if anchor != sanitized_anchor:
                        link['href'] = '#' + sanitized_anchor
                        self.log(f"  → Sanitized internal anchor: {href} → #{sanitized_anchor}")
                continue
                
            # Parse the URL to handle fragments
            parsed = urlparse(href)
            path_part = unquote(parsed.path)
            
            # Check if this is an HTML file reference OR an MD file reference
            if path_part.endswith(('.html', '.htm', '.xhtml', '.xhtm', '.HTML', '.HTM', '.XHTML', '.XHTM', '.md', '.MD')):
                # Skip processing if it already ends with .md (unless we need to handle fragment)
                if path_part.endswith(('.md', '.MD')) and not parsed.fragment:
                    # Already pointing to .md file and no fragment to process
                    continue
                
                # For .md files with fragments, we need to process the fragment but keep the path
                if path_part.endswith(('.md', '.MD')):
                    # Just use the path as-is since it's already .md
                    new_href = path_part
                    
                    # Process fragment if present
                    if parsed.fragment:
                        fragment = unquote(parsed.fragment)
                        
                        # Check if the fragment itself ends with .md (which would be unusual)
                        if fragment.endswith('.md'):
                            # This is likely an error in the source - log it and strip the .md
                            self.log(f"  → Warning: Fragment '{fragment}' ends with .md - this is likely an error")
                            fragment = fragment[:-3]  # Remove the .md extension
                        
                        # Process the fragment as usual
                        if self.docusaurus:
                            # Sanitize and convert to Docusaurus format
                            sanitized_fragment = fragment.replace(':', '_').replace('&', '_and_')
                            sanitized_fragment = sanitized_fragment.lstrip('_')
                            docusaurus_id = self.madcap_to_docusaurus_id(sanitized_fragment)
                            new_href += '#' + docusaurus_id
                        else:
                            # Just sanitize
                            sanitized_fragment = fragment.replace(':', '_').replace('&', '_and_')
                            sanitized_fragment = sanitized_fragment.lstrip('_')
                            new_href += '#' + sanitized_fragment
                    
                    # Update the link
                    link['href'] = new_href
                    self.log(f"  → Updated .md link: {href} → {new_href}")
                    continue
                
                # If lowercase mode is enabled, handle paths differently
                if self.lowercase_filenames:
                    # For relative paths, we need to handle them component by component
                    if not path_part.startswith('/'):
                        # It's a relative path
                        # Normalize the path (resolve .. and .)
                        current_dir = Path(html_file).parent
                        resolved_path = (current_dir / path_part).resolve()
                        
                        try:
                            # Get the resolved path relative to input directory
                            rel_to_input = resolved_path.relative_to(self.input_dir)
                            
                            # Apply transformations (flatten and lowercase)
                            flattened = self.flatten_path(rel_to_input)
                            final_path = self.lowercase_path(flattened)
                            
                            # Get current file's transformed path
                            current_rel = html_file.relative_to(self.input_dir)
                            current_flattened = self.flatten_path(current_rel)
                            current_final = self.lowercase_path(current_flattened)
                            
                            # Calculate the relative path between transformed locations
                            target_md = (self.output_dir / final_path).with_suffix('.md')
                            current_md_dir = (self.output_dir / current_final).parent
                            
                            # Use os.path.relpath to get the relative path
                            new_path = Path(os.path.relpath(target_md, current_md_dir))
                        except ValueError:
                            # Fallback: just lowercase all components of the original path
                            path_obj = Path(path_part)
                            parts = list(path_obj.parts)
                            # Lowercase all parts including directories
                            lowercased_parts = []
                            for part in parts:
                                if '.' in part and part == parts[-1]:  # It's the filename
                                    name, ext = part.rsplit('.', 1)
                                    lowercased_parts.append(name.lower() + '.' + ext)
                                else:
                                    lowercased_parts.append(part.lower())
                            new_path = Path(*lowercased_parts).with_suffix('.md')
                    else:
                        # Absolute path - just lowercase all components
                        path_obj = Path(path_part)
                        parts = list(path_obj.parts)
                        lowercased_parts = [p.lower() for p in parts]
                        new_path = Path(*lowercased_parts).with_suffix('.md')
                elif self.flatten_dirs:
                    # Just flattening, no lowercase
                    ref_path = (Path(html_file).parent / path_part).resolve()
                    try:
                        target_rel = ref_path.relative_to(self.input_dir)
                        target_flattened = self.flatten_path(target_rel)
                        
                        current_rel = html_file.relative_to(self.input_dir)
                        current_flattened = self.flatten_path(current_rel)
                        
                        new_path = os.path.relpath(
                            self.output_dir / target_flattened.with_suffix('.md'),
                            (self.output_dir / current_flattened).parent
                        )
                        new_path = Path(new_path)
                    except ValueError:
                        # Fallback
                        new_path = Path(path_part).with_suffix('.md')
                else:
                    # No transformation, just update extension
                    new_path = Path(path_part).with_suffix('.md')
                
                # Reconstruct the URL with the new path
                new_href = str(new_path).replace('\\', '/')
                
                # Handle fragment - don't lowercase fragments as they are case-sensitive anchors
                if parsed.fragment:
                    fragment = unquote(parsed.fragment)
                    
                    # Fix known broken anchor references
                    if (new_href.endswith('permissions.md') and 
                        fragment == 'Grant Permissions to the Registered Application'):
                        # This anchor doesn't exist in permissions.md, it's in registerconfig.md
                        new_href = new_href.replace('permissions.md', 'registerconfig.md')
                        new_href += '#Grant'
                        self.log(f"  → Fixed broken anchor reference: redirected to registerconfig.md#Grant")
                    # Handle more generic case where fragment might be in wrong file
                    elif hasattr(self, 'global_truncated_mappings') and fragment in self.global_truncated_mappings:
                        # Check if the anchor exists in a different file
                        candidates = self.global_truncated_mappings[fragment]
                        target_file_key = str(new_path).replace('\\', '/')
                        
                        # If we can't find it in the target file, look for it elsewhere
                        found_in_target = False
                        for file_key, heading_text in candidates:
                            if file_key == target_file_key:
                                found_in_target = True
                                break
                        
                        if not found_in_target and candidates:
                            # Use the first candidate file that has this anchor
                            correct_file_key, heading_text = candidates[0]
                            # Update the href to point to the correct file
                            new_href = new_href.rsplit('/', 1)[0] + '/' + correct_file_key.rsplit('/', 1)[-1]
                            self.log(f"  → Redirected anchor '{fragment}' from {target_file_key} to {correct_file_key}")
                            # Don't continue to else - fall through to process the anchor
                    
                    if True:  # Always process the anchor after potential redirect
                        # For Docusaurus, convert to Docusaurus-style IDs
                        if self.docusaurus:
                            # First do the basic sanitization
                            sanitized_fragment = fragment.replace(':', '_').replace('&', '_and_')
                            sanitized_fragment = sanitized_fragment.lstrip('_')
                            
                            # Check if this is a truncated MadCap anchor (8 characters or less)
                            is_truncated = len(fragment) <= 8 and not '-' in fragment
                            
                            # If we have a heading mapping for this anchor, use the heading text
                            # to generate the Docusaurus ID
                            docusaurus_id = None
                            
                            # Try to resolve using global mappings (for cross-file references)
                            if hasattr(self, 'global_anchor_mappings'):
                                # We need to resolve the relative path to match our global mapping keys
                                # The new_path might be relative (like ../../Configuration/EntraID/RegisterConfig.md)
                                # We need to convert it to the format used in global_anchor_mappings
                                try:
                                    # Get the current file's output path relative to output directory
                                    current_rel = html_file.relative_to(self.input_dir)
                                    if self.flatten_dirs:
                                        current_rel = self.flatten_path(current_rel)
                                    if self.lowercase_filenames:
                                        current_rel = self.lowercase_path(current_rel)
                                    current_output = current_rel.with_suffix('.md')
                                    
                                    # Resolve the target path
                                    if not str(new_path).startswith('/'):
                                        # It's a relative path - resolve it
                                        target_abs = (current_output.parent / new_path).resolve()
                                        # Make it relative to output_dir to match our keys
                                        try:
                                            # This is a bit tricky - we need to figure out the path relative to the root
                                            # We'll construct it by removing the common prefix
                                            parts = list(target_abs.parts)
                                            # Find where the path starts to match our expected structure
                                            for i, part in enumerate(parts):
                                                if part.lower() in ['1secure', 'accessanalyzer', 'productname']:
                                                    target_file_key = '/'.join(parts[i:])
                                                    break
                                            else:
                                                # Fallback - use the path as-is
                                                target_file_key = str(new_path).replace('\\', '/')
                                        except:
                                            target_file_key = str(new_path).replace('\\', '/')
                                    else:
                                        target_file_key = str(new_path).replace('\\', '/').lstrip('/')
                                    
                                    # Ensure lowercase if needed
                                    if self.lowercase_filenames:
                                        target_file_key = target_file_key.lower()
                                    
                                except Exception as e:
                                    # Fallback to simple normalization
                                    target_file_key = str(new_path).replace('\\', '/')
                                    if self.verbose:
                                        self.log(f"  → Path resolution error: {e}")
                                
                                if self.verbose:
                                    self.log(f"  → Looking for cross-file anchor '{fragment}' in file '{target_file_key}'")
                                    # Debug: show available keys
                                    matching_keys = [k for k in self.global_anchor_mappings.keys() if 'registerconfig' in k.lower()]
                                    if matching_keys:
                                        self.log(f"  → Found similar keys: {matching_keys}")
                                
                                # Check if we have mappings for the target file
                                if target_file_key in self.global_anchor_mappings:
                                    file_mappings = self.global_anchor_mappings[target_file_key]
                                    
                                    # Try exact match
                                    if fragment in file_mappings:
                                        heading_text = file_mappings[fragment]
                                        docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                        self.log(f"  → Found cross-file anchor mapping: {fragment} → {heading_text}")
                                    # Check if we have the Docusaurus ID already computed
                                    elif fragment + '_docusaurus' in file_mappings:
                                        docusaurus_id = file_mappings[fragment + '_docusaurus']
                                        self.log(f"  → Found pre-computed Docusaurus ID: {fragment} → {docusaurus_id}")
                                
                                # If not found and looks truncated, check global truncated mappings
                                if not docusaurus_id and is_truncated and hasattr(self, 'global_truncated_mappings'):
                                    if fragment in self.global_truncated_mappings:
                                        # Find which file this anchor refers to
                                        candidates = self.global_truncated_mappings[fragment]
                                        for file_key, heading_text in candidates:
                                            if file_key == target_file_key:
                                                docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                                self.log(f"  → Found truncated cross-file anchor: {fragment} → {heading_text}")
                                                break
                                
                                # If still not found, search all files for this anchor
                                if not docusaurus_id:
                                    # Search through all files for this anchor
                                    found = False
                                    if self.verbose:
                                        self.log(f"  → Searching all files for anchor '{fragment}'")
                                    
                                    for file_key, file_anchors in self.global_anchor_mappings.items():
                                        if fragment in file_anchors:
                                            # Check if this is likely the right file based on the path
                                            if 'registerconfig' in file_key.lower() and 'registerconfig' in new_href.lower():
                                                heading_text = file_anchors[fragment]
                                                docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                                self.log(f"  → Found cross-file anchor by search: {fragment} → {heading_text} in {file_key}")
                                                found = True
                                                break
                                            elif self.verbose:
                                                self.log(f"  → Found '{fragment}' in {file_key} but path doesn't match")
                                    
                                    # Also check truncated mappings
                                    if not found and is_truncated and hasattr(self, 'global_truncated_mappings'):
                                        if fragment in self.global_truncated_mappings:
                                            candidates = self.global_truncated_mappings[fragment]
                                            # If there's only one candidate or if the filename matches, use it
                                            for file_key, heading_text in candidates:
                                                if 'registerconfig' in file_key.lower() and 'registerconfig' in new_href.lower():
                                                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                                    self.log(f"  → Found truncated cross-file anchor by search: {fragment} → {heading_text} in {file_key}")
                                                    break
                            
                            # Fall back to local mappings if global lookup failed
                            if not docusaurus_id:
                                # First check if we have a direct mapping from the original anchor ID
                                if hasattr(self, 'original_anchor_mappings') and fragment in self.original_anchor_mappings:
                                    heading_text = self.original_anchor_mappings[fragment]
                                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                    self.log(f"  → Found original anchor mapping: {fragment} → {heading_text}")
                                
                                # Next check if this is a known truncated anchor
                                elif hasattr(self, 'truncated_anchor_mappings') and fragment in self.truncated_anchor_mappings:
                                    heading_text = self.truncated_anchor_mappings[fragment]
                                    docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                    self.log(f"  → Found truncated anchor mapping: {fragment} → {heading_text}")
                                
                                # Otherwise check regular mappings
                                elif hasattr(self, 'anchor_mappings'):
                                    # First try exact match
                                    for heading_text, anchor_id in self.anchor_mappings.items():
                                        if anchor_id == sanitized_fragment:
                                            # Generate ID from heading text like Docusaurus does
                                            docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                            break
                                    
                                    # If no exact match and this looks like a truncated anchor,
                                    # try to find a heading that starts with this truncated text
                                    if not docusaurus_id and is_truncated:
                                        for heading_text, anchor_id in self.anchor_mappings.items():
                                            # Check if the anchor ID starts with the truncated version
                                            if anchor_id.lower().startswith(fragment.lower()):
                                                docusaurus_id = self.madcap_to_docusaurus_id(heading_text)
                                                self.log(f"  → Matched truncated anchor '{fragment}' to heading '{heading_text}'")
                                                break
                            
                            # If we found a mapping, use the Docusaurus ID
                            # Otherwise, convert the anchor ID itself
                            if docusaurus_id:
                                new_href += '#' + docusaurus_id
                                self.log(f"  → Converted anchor to Docusaurus format: {fragment} → {docusaurus_id}")
                            else:
                                # Convert the anchor ID directly
                                docusaurus_id = self.madcap_to_docusaurus_id(sanitized_fragment)
                                new_href += '#' + docusaurus_id
                                self.log(f"  → Converted anchor to Docusaurus format: {fragment} → {docusaurus_id}")
                        else:
                            # Non-Docusaurus mode - just sanitize
                            sanitized_fragment = fragment.replace(':', '_').replace('&', '_and_')
                            sanitized_fragment = sanitized_fragment.lstrip('_')
                            new_href += '#' + sanitized_fragment
                            if fragment != sanitized_fragment:
                                self.log(f"  → Sanitized anchor: {fragment} → {sanitized_fragment}")
                if parsed.query:
                    new_href += '?' + parsed.query
                    
                link['href'] = new_href
                self.log(f"  → Updated link: {href} → {new_href}")
    
    def preserve_heading_ids(self, soup):
        """Preserve heading IDs by storing them for later MDX-compatible processing"""
        # Common words that are often used as fragment IDs
        common_fragment_words = {
            'overview', 'introduction', 'review', 'install', 'configure', 
            'setup', 'requirements', 'prerequisites', 'grant', 'assign',
            'create', 'add', 'delete', 'modify', 'update', 'manage'
        }
        
        # Track used anchor IDs to ensure uniqueness
        used_anchor_ids = set()
        
        # Store anchor mappings for later use
        self.anchor_mappings = {}
        
        # Also check for anchor tags that might be right before or after headings
        # MadCap often puts anchors as separate elements
        all_anchors = {}
        for anchor in soup.find_all('a', {'name': True}):
            if anchor.get('name'):
                all_anchors[anchor.get('name')] = anchor
        
        # Process headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            # Check for existing 'name' or 'id' attributes
            anchor_id = heading.get('name') or heading.get('id')
            
            # Also check for anchor tags within the heading
            anchor = heading.find('a', {'name': True})
            if anchor and not anchor_id:
                anchor_id = anchor.get('name')
                # Remove the anchor tag but keep its content
                anchor.unwrap()
            
            # Check if there's an anchor right before this heading
            if not anchor_id:
                prev_sibling = heading.find_previous_sibling()
                if prev_sibling and prev_sibling.name == 'a' and prev_sibling.get('name'):
                    anchor_id = prev_sibling.get('name')
                    # Remove the standalone anchor tag
                    prev_sibling.extract()
                    self.log(f"  → Found anchor before heading: {anchor_id}")
            
            heading_text = heading.get_text(strip=True)
            if not heading_text:
                continue
                
            # If heading already has an ID, preserve it
            if anchor_id:
                # Sanitize anchor ID for MDX compatibility
                # Replace colons and other invalid characters with underscores
                sanitized_anchor_id = anchor_id.replace(':', '_').replace('&', '_and_')
                # Remove leading underscores as they're not valid in HTML5/React IDs
                sanitized_anchor_id = sanitized_anchor_id.lstrip('_')
                
                # Ensure uniqueness
                original_sanitized = sanitized_anchor_id
                counter = 1
                while sanitized_anchor_id in used_anchor_ids:
                    sanitized_anchor_id = f"{original_sanitized}_{counter}"
                    counter += 1
                
                used_anchor_ids.add(sanitized_anchor_id)
                
                # Store the mapping for later use
                self.anchor_mappings[heading_text] = sanitized_anchor_id
                
                # Also store a direct mapping from the original anchor ID to heading text
                # This is crucial for MadCap's truncated anchors
                if not hasattr(self, 'original_anchor_mappings'):
                    self.original_anchor_mappings = {}
                self.original_anchor_mappings[anchor_id] = heading_text
                
                # Also store the truncated version if MadCap would truncate it
                if len(anchor_id) > 8 and not '-' in anchor_id:
                    truncated_id = anchor_id[:8]
                    # Store a mapping from truncated to full anchor ID
                    if not hasattr(self, 'truncated_anchor_mappings'):
                        self.truncated_anchor_mappings = {}
                    self.truncated_anchor_mappings[truncated_id] = heading_text
                    self.log(f"  → Stored truncated anchor mapping: {truncated_id} → {heading_text}")
                
                # Add data attribute to preserve the anchor ID
                heading['data-anchor-id'] = sanitized_anchor_id
                
                if original_sanitized != sanitized_anchor_id:
                    self.log(f"  → Preserved heading ID (made unique): {anchor_id} → {sanitized_anchor_id}")
                else:
                    self.log(f"  → Preserved heading ID: {anchor_id} → {sanitized_anchor_id}")
            else:
                # For h1 tags, create MadCap-style implicit anchors
                if heading.name == 'h1':
                    # MadCap creates implicit anchors from h1 text by replacing spaces with underscores
                    implicit_anchor = heading_text.replace(' ', '_')
                    
                    # Ensure uniqueness
                    original_anchor = implicit_anchor
                    counter = 1
                    while implicit_anchor in used_anchor_ids:
                        implicit_anchor = f"{original_anchor}_{counter}"
                        counter += 1
                    
                    used_anchor_ids.add(implicit_anchor)
                    
                    # Store the mapping
                    self.anchor_mappings[heading_text] = implicit_anchor
                    
                    # Add data attribute
                    heading['data-anchor-id'] = implicit_anchor
                    
                    self.log(f"  → Added MadCap implicit anchor for h1: {implicit_anchor}")
                else:
                    # Check if the heading starts with a common fragment word
                    first_word = heading_text.split()[0] if heading_text.split() else ""
                    if first_word:
                        first_word_lower = first_word.lower()
                        # If the first word is commonly used as a fragment, add it as ID
                        if first_word_lower in common_fragment_words:
                            # Use the original case of the first word as the ID
                            # Ensure uniqueness
                            anchor_to_use = first_word
                            original_anchor = anchor_to_use
                            counter = 1
                            while anchor_to_use in used_anchor_ids:
                                anchor_to_use = f"{original_anchor}_{counter}"
                                counter += 1
                            
                            used_anchor_ids.add(anchor_to_use)
                            
                            # Store the mapping
                            self.anchor_mappings[heading_text] = anchor_to_use
                            
                            # Add data attribute
                            heading['data-anchor-id'] = anchor_to_use
                            
                            self.log(f"  → Added common heading ID: {anchor_to_use}")
        
        # Handle standalone anchors
        for name, anchor in all_anchors.items():
            # Check if this anchor is already handled
            if anchor.parent is None:
                continue
                
            # Check if this anchor is already handled (inside or before a heading)
            next_elem = anchor.find_next_sibling()
            if next_elem and next_elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Already handled above
                continue
            
            # For standalone anchors, we'll need to create invisible markers
            # that can be processed later
            try:
                # Sanitize anchor name for MDX compatibility
                sanitized_name = name.replace(':', '_').replace('&', '_and_')
                # Remove leading underscores as they're not valid in HTML5/React IDs
                sanitized_name = sanitized_name.lstrip('_')
                
                # Ensure uniqueness
                original_sanitized = sanitized_name
                counter = 1
                while sanitized_name in used_anchor_ids:
                    sanitized_name = f"{original_sanitized}_{counter}"
                    counter += 1
                
                used_anchor_ids.add(sanitized_name)
                
                # Create a span with data attribute to preserve the anchor
                marker = soup.new_tag('span')
                marker['data-anchor-id'] = sanitized_name
                marker['style'] = 'display:none'
                marker.string = f"[anchor:{sanitized_name}]"
                anchor.replace_with(marker)
                
                if original_sanitized != sanitized_name:
                    self.log(f"  → Preserved standalone anchor (made unique): {name} → {sanitized_name}")
                else:
                    self.log(f"  → Preserved standalone anchor: {name} → {sanitized_name}")
            except Exception as e:
                self.log(f"  → Could not preserve anchor {name}: {str(e)}")
                
    def clean_madcap_elements(self, soup):
        """Remove MadCap Flare specific elements"""
        # Remove any elements that might contain /* */ patterns
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and '/*' in text and '*/' in text):
            if comment.strip() == '/* */':
                comment.extract()
        
        # Remove MadCap conditional text markers
        for element in soup.find_all(attrs={'madcap:conditions': True}):
            element.unwrap()
            
        # Remove MadCap dropdowns
        for dropdown in soup.find_all(class_='MCDropDown'):
            dropdown.unwrap()
            
        # Remove empty paragraphs (but not if they contain images)
        for p in soup.find_all('p'):
            if not p.get_text(strip=True) and not p.find_all('img'):
                p.decompose()
                
        # Fix self-closing tags that might cause issues
        # BeautifulSoup should handle most of these, but let's be sure
        for tag in soup.find_all():
            # Remove problematic attributes that might contain invalid characters
            if tag.attrs:
                for attr in list(tag.attrs.keys()):
                    if '/' in attr or '<' in attr or '>' in attr:
                        del tag.attrs[attr]
        
        # Special handling for command line code blocks split across multiple p tags
        # Pattern: consecutive p tags with classes like Command-Line-1, Command-Line-2, etc.
        all_p_tags = soup.find_all('p')
        i = 0
        while i < len(all_p_tags):
            p = all_p_tags[i]
            if p.get('class') and any('Command-Line' in cls for cls in p.get('class', [])):
                # Found start of a command line block
                code_lines = []
                j = i
                
                # Collect all consecutive Command-Line paragraphs
                while j < len(all_p_tags):
                    current_p = all_p_tags[j]
                    if current_p.get('class') and any('Command-Line' in cls for cls in current_p.get('class', [])):
                        # Get text content and decode entities
                        text = current_p.get_text()
                        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                        code_lines.append(text)
                        j += 1
                    else:
                        break
                
                if len(code_lines) > 1:  # Only process if we found multiple lines
                    # Create a pre tag with all the content
                    pre_tag = soup.new_tag('pre')
                    code_tag = soup.new_tag('code')
                    code_tag.string = '\n'.join(code_lines)
                    pre_tag.append(code_tag)
                    
                    # Replace the first p tag with the pre tag
                    all_p_tags[i].replace_with(pre_tag)
                    
                    # Remove the remaining p tags
                    for k in range(i + 1, j):
                        if k < len(all_p_tags):
                            all_p_tags[k].decompose()
                    
                    # Skip past the processed tags
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        # Special handling for code snippets with syntax highlighting
        # These have complex span structures that need to be preserved
        for div in soup.find_all('div', class_='codeSnippetBody'):
            # Check if there's a pre/code inside
            pre_code = div.find('pre')
            if pre_code:
                # First, replace <br> and <br/> tags with newlines
                for br in pre_code.find_all(['br', 'BR']):
                    br.replace_with('\n')
                
                # Remove all span tags but keep their content
                for span in pre_code.find_all('span'):
                    span.unwrap()
                
                # Get the text content with preserved line breaks
                code_text = pre_code.get_text()
                
                # Replace HTML entities
                code_text = code_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&#160;', ' ')
                
                # Clean up excessive whitespace but preserve intentional indentation
                lines = code_text.split('\n')
                cleaned_lines = []
                for line in lines:
                    # Preserve leading whitespace but strip trailing
                    cleaned_lines.append(line.rstrip())
                code_text = '\n'.join(cleaned_lines)
                
                # Update the pre tag content
                # Create a new code tag with the cleaned content
                pre_code.clear()
                code_tag = soup.new_tag('code')
                code_tag.string = code_text
                pre_code.append(code_tag)
                
    def fix_solo_backticks(self, content):
        """Fix solo backticks and solo double backticks by converting them to triple backticks"""
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            # Track if we're in a code block
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue
            
            # Don't process lines inside code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Pattern 1: Solo backtick with spaces around it (e.g., " ` ")
            # But not if it's part of inline code (e.g., `code`)
            line = re.sub(r'(?<![`\w])` (?![`\w])', ' ``` ', line)
            
            # Pattern 2: Solo backtick at the beginning of a line
            if line.strip() == '`':
                line = line.replace('`', '```')
            elif re.match(r'^\s*`\s*$', line):
                # Solo backtick with only whitespace
                line = re.sub(r'^(\s*)`(\s*)$', r'\1```\2', line)
            elif re.match(r'^\s*`\s+', line) and line.count('`') == 1:
                # Backtick at start of line followed by space and text, with no closing backtick
                line = re.sub(r'^(\s*)`(\s+)', r'\1```\2', line)
            
            # Pattern 3: Solo double backticks with spaces around them (e.g., " `` ")
            line = re.sub(r'(?<![`\w])`` (?![`\w])', ' ``` ', line)
            
            # Pattern 4: Solo double backticks at the beginning/end of a line
            if line.strip() == '``':
                line = line.replace('``', '```')
            elif re.match(r'^\s*``\s*$', line):
                # Solo double backticks with only whitespace
                line = re.sub(r'^(\s*)``(\s*)$', r'\1```\2', line)
            elif re.match(r'^\s*``\s+', line) and line.count('`') == 2:
                # Double backticks at start followed by space and text, with no other backticks
                line = re.sub(r'^(\s*)``(\s+)', r'\1```\2', line)
            
            # Pattern 5: Solo backticks in the middle of text (more aggressive)
            # Only if there's an odd number of backticks (meaning unpaired)
            if line.count('`') % 2 == 1:
                # Check if it's a solo backtick after text
                line = re.sub(r'([^`\s])(\s+)`(\s+)([^`])', r'\1\2```\3\4', line)
                # Check if it's a solo backtick before punctuation
                line = re.sub(r'([^`\s])(\s+)`([.,;:!?\s])', r'\1\2```\3', line)
            
            # Pattern 6: Double backticks in the middle that aren't inline code
            if '``' in line and not re.search(r'``[^`]+``', line):
                # Replace double backticks that aren't part of inline code blocks
                line = re.sub(r'([^`])``([^`])', r'\1```\2', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def should_wrap_curly_brace(self, brace_content):
        """Check if a curly brace pattern should be wrapped in backticks"""
        # Skip if it's a heading anchor
        if brace_content.startswith('{#'):
            return False
            
        # Patterns that should be wrapped
        patterns = [
            r'^\{\$\w+\}$',  # PowerShell variables: {$guid}, {$variable}
            r'^\{[A-Z][A-Z0-9_\\\\]*\}$',  # Template variables: {JOB_GUID}
            r'^\{insert [^}]+\}$',  # Placeholder patterns: {insert value here}
            r'^\{your [^}]+\}$',  # {your text}
            r'^\{[A-Z][a-z]+ of [^}]+\}$',  # Path placeholders: {Location of ...}
            r'^\{[a-z][a-zA-Z0-9_]*\}$',  # Mixed case single words: {HostName}, {userId}
            r'^\{[0-9]+\}$',  # Numeric placeholders: {0}, {1}, {123}
        ]
        
        for pattern in patterns:
            if re.match(pattern, brace_content):
                return True
        
        return False
    
    def fix_curly_braces_in_line(self, line):
        """Fix curly braces in a single line to prevent MDX interpretation as JSX"""
        # Skip heading anchors
        if '{#' in line:
            return line
        
        # Check if this line contains markdown links
        # If so, we need to be careful not to break them
        if '](' in line:
            # Process the line in segments, skipping content inside markdown links
            result = ""
            i = 0
            while i < len(line):
                # Check if we're at the start of a markdown link
                if i < len(line) - 1 and line[i] == ']' and line[i+1] == '(':
                    # Found start of link, copy everything up to and including ']('
                    result += line[i:i+2]
                    i += 2
                    
                    # Find the end of the link (closing parenthesis)
                    paren_count = 1
                    link_content = ""
                    while i < len(line) and paren_count > 0:
                        if line[i] == '(':
                            paren_count += 1
                        elif line[i] == ')':
                            paren_count -= 1
                        
                        if paren_count > 0:
                            link_content += line[i]
                        i += 1
                    
                    # Add the link content without processing it
                    result += link_content + ')'
                else:
                    # Not in a link, collect characters until we find a link or curly brace
                    segment = ""
                    while i < len(line) and not (i < len(line) - 1 and line[i] == ']' and line[i+1] == '(') and line[i] != '{':
                        segment += line[i]
                        i += 1
                    
                    result += segment
                    
                    # If we found a curly brace (and we're not at a link), process it
                    if i < len(line) and line[i] == '{':
                        # Find the closing brace
                        brace_content = "{"
                        i += 1
                        while i < len(line) and line[i] != '}':
                            brace_content += line[i]
                            i += 1
                        if i < len(line):
                            brace_content += '}'
                            i += 1
                        
                        # Check if this curly brace pattern should be wrapped
                        if self.should_wrap_curly_brace(brace_content):
                            result += f'`{brace_content}`'
                        else:
                            result += brace_content
            
            return result
        
        # For lines without any backticks or links, wrap curly brace patterns
        if '`' not in line:
            # Common patterns that need to be wrapped in backticks
            patterns = [
                # PowerShell variables: {$guid}, {$variable}
                (r'\{\$\w+\}', lambda m: f'`{m.group(0)}`'),
                # Template variables: {JOB_GUID}, {HOSTNAME}, {SCAN_TYPE}
                # Also handle escaped underscores from markdownify: {JOB\_GUID}
                (r'\{[A-Z][A-Z0-9_\\\\]*\}', lambda m: f'`{m.group(0)}`'),
                # Placeholder patterns: {insert value here}, {your text}
                (r'\{insert [^}]+\}', lambda m: f'`{m.group(0)}`'),
                (r'\{your [^}]+\}', lambda m: f'`{m.group(0)}`'),
                # Path placeholders: {Location of ...}
                (r'\{[A-Z][a-z]+ of [^}]+\}', lambda m: f'`{m.group(0)}`'),
                # Mixed case single words: {HostName}, {userId}, etc
                (r'\{[a-z][a-zA-Z0-9_]*\}', lambda m: f'`{m.group(0)}`'),
                # Numeric or special placeholders: {0}, {1}, {123}
                (r'\{[0-9]+\}', lambda m: f'`{m.group(0)}`'),
            ]
            
            # Apply patterns
            for pattern, replacement in patterns:
                line = re.sub(pattern, replacement, line)
            
            # Handle inline code patterns like appid={$guid}
            # Look for patterns like word={$something} or word={SOMETHING}
            line = re.sub(r'(\w+)=\{([$A-Z][^}]*)\}', r'\1=`{\2}`', line)
            
            return line
        
        # For lines with backticks, we need to be more careful
        # Split the line into segments inside and outside of backticks
        segments = []
        in_backticks = False
        current_segment = ""
        
        i = 0
        while i < len(line):
            if line[i] == '`':
                # Found a backtick, toggle state
                if current_segment:
                    segments.append((current_segment, in_backticks))
                    current_segment = ""
                in_backticks = not in_backticks
                current_segment += '`'
            else:
                current_segment += line[i]
            i += 1
        
        # Add the last segment
        if current_segment:
            segments.append((current_segment, in_backticks))
        
        # Process each segment
        result = ""
        for segment, was_in_backticks in segments:
            if was_in_backticks:
                # Don't modify content inside backticks
                result += segment
            else:
                # Apply patterns to content outside backticks
                processed = segment
                
                # Common patterns that need to be wrapped in backticks
                patterns = [
                    # PowerShell variables: {$guid}, {$variable}
                    (r'\{\$\w+\}', lambda m: f'`{m.group(0)}`'),
                    # Template variables: {JOB_GUID}, {HOSTNAME}, {SCAN_TYPE}
                    # Also handle escaped underscores from markdownify: {JOB\_GUID}
                    (r'\{[A-Z][A-Z0-9_\\\\]*\}', lambda m: f'`{m.group(0)}`'),
                    # Placeholder patterns: {insert value here}, {your text}
                    (r'\{insert [^}]+\}', lambda m: f'`{m.group(0)}`'),
                    (r'\{your [^}]+\}', lambda m: f'`{m.group(0)}`'),
                    # Path placeholders: {Location of ...}
                    (r'\{[A-Z][a-z]+ of [^}]+\}', lambda m: f'`{m.group(0)}`'),
                    # Mixed case single words: {HostName}, {userId}, etc
                    (r'\{[a-z][a-zA-Z0-9_]*\}', lambda m: f'`{m.group(0)}`'),
                    # Numeric or special placeholders: {0}, {1}, {123}
                    (r'\{[0-9]+\}', lambda m: f'`{m.group(0)}`'),
                ]
                
                # Apply patterns
                for pattern, replacement in patterns:
                    processed = re.sub(pattern, replacement, processed)
                
                # Special handling for log format patterns
                # [TIME]_{JOB_GUID}_[SessionID].log -> [TIME]_`{JOB_GUID}`_[SessionID].log
                processed = re.sub(r'(\[[^\]]+\]_)\{([^}]+)\}(_\[[^\]]+\])', r'\1`{\2}`\3', processed)
                
                # Handle inline code patterns like appid={$guid}
                # Look for patterns like word={$something} or word={SOMETHING}
                processed = re.sub(r'(\w+)=\{([$A-Z][^}]*)\}', r'\1=`{\2}`', processed)
                
                result += processed
        
        return result
    
    def madcap_to_docusaurus_id(self, anchor_id):
        """Convert MadCap anchor ID to Docusaurus-style ID"""
        # Docusaurus generates IDs by:
        # 1. Converting to lowercase
        # 2. Replacing spaces and underscores with hyphens
        # 3. Removing special characters
        
        # Start with the anchor ID
        docusaurus_id = anchor_id
        
        # Replace & with 'and' before removing special characters
        docusaurus_id = docusaurus_id.replace('&', 'and')
        
        # Convert to lowercase
        docusaurus_id = docusaurus_id.lower()
        
        # Replace underscores and spaces with hyphens
        docusaurus_id = re.sub(r'[_\s]+', '-', docusaurus_id)
        
        # Remove special characters (keep only alphanumeric and hyphens)
        docusaurus_id = re.sub(r'[^a-z0-9-]', '', docusaurus_id)
        
        # Remove leading/trailing hyphens
        docusaurus_id = docusaurus_id.strip('-')
        
        # Collapse multiple hyphens
        docusaurus_id = re.sub(r'-+', '-', docusaurus_id)
        
        return docusaurus_id
    
    def restore_heading_anchors(self, content):
        """Keep headings as plain markdown - don't add HTML anchors"""
        # This method is now a no-op since we're not adding HTML headings
        # Docusaurus will generate its own IDs from the heading text
        return content
    
    def restore_mdx_anchors(self, content):
        """Restore anchors in MDX-compatible format"""
        if not self.docusaurus or not hasattr(self, 'anchor_mappings'):
            return content
        
        lines = content.split('\n')
        new_lines = []
        in_frontmatter = False
        frontmatter_count = 0
        
        for line in lines:
            # Track frontmatter
            if line.strip() == '---':
                frontmatter_count += 1
                in_frontmatter = frontmatter_count == 1
                new_lines.append(line)
                continue
            
            # Skip frontmatter lines
            if in_frontmatter:
                new_lines.append(line)
                continue
            
            # Check for standalone anchor markers
            if '[anchor:' in line:
                # Extract anchor ID
                match = re.search(r'\[anchor:([^\]]+)\]', line)
                if match:
                    anchor_id = match.group(1)
                    # For MDX, we can use an invisible span with an id
                    # This is MDX-compatible
                    # Unescape any escaped characters in the anchor ID
                    anchor_id = anchor_id.replace('\\_', '_')
                    anchor_html = f'<span id="{anchor_id}"></span>'
                    new_line = line.replace(match.group(0), anchor_html)
                    new_lines.append(new_line)
                    self.log(f"  → Restored standalone anchor as span: {anchor_id}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def clean_markdown(self, content):
        """Clean up the converted markdown"""
        # Debug: Count code blocks at start
        if self.verbose and '```' in content:
            code_blocks_before = len(re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL))
            self.log(f"  → clean_markdown: {code_blocks_before} code blocks at start")
        
        # Remove navigation elements and other non-content elements
        lines = content.split('\n')
        cleaned_lines = []
        skip_until = 0
        
        for i, line in enumerate(lines):
            # Skip common navigation patterns
            if any(pattern in line.lower() for pattern in [
                'skip to main content',
                'you are here:',
                'submit search',
                'filter:',
                '- all files',
                'account',
                'settings',
                'logout',
                '- placeholder'
            ]):
                continue
                
            # Skip lines that are just "---" unless they're part of a table
            if line.strip() == '---' and (i == 0 or i < 30):
                continue
                
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove excessive blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Fix image syntax if needed
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'![\1](\2)', content)
        
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Remove any lines that look like JavaScript (but not in code blocks)
        lines = content.split('\n')
        cleaned_lines = []
        skip_js_block = False
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                cleaned_lines.append(line)
                continue
                
            # Don't process lines inside code blocks
            if in_code_block:
                cleaned_lines.append(line)
                continue
            
            # Detect start of JS block
            if '/* <![CDATA[' in line or 'window.dataLayer' in line or 'function gtag()' in line:
                skip_js_block = True
                continue
            # Detect end of JS block
            elif skip_js_block and ('/* ]]>' in line or '*/]]>' in line or ']]> */' in line):
                skip_js_block = False
                continue
            # Skip lines in JS block
            elif skip_js_block:
                continue
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove empty CSS comments that show up as /* */
        content = re.sub(r'/\*\s*\*/', '', content)
        # Also remove them if they're on their own line
        content = re.sub(r'^\s*/\*\s*\*/\s*$', '', content, flags=re.MULTILINE)
        # Remove escaped versions too (this is what we're seeing)
        content = re.sub(r'/\\\*\s*\\\*/', '', content)
        # Remove with newlines around them
        content = re.sub(r'\n\s*/\\\*\s*\\\*/\s*\n', '\n\n', content)
        # Also try without escaping in the regex
        content = content.replace('/\\* \\*/', '')
        # Try the exact pattern we're seeing
        content = content.replace('/\\*  \\*/', '')
        
        # Debug: Check code blocks before escape_custom_tags
        if self.verbose and '```' in content:
            code_blocks_before_escape = re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL)
            self.log(f"  → Before escape_custom_tags: {len(code_blocks_before_escape)} code blocks")
            for idx, block in enumerate(code_blocks_before_escape):
                content_preview = block[:50] + '...' if len(block) > 50 else block
                self.log(f"    Block {idx + 1}: {repr(content_preview)}")
        
        # Escape custom configuration tags first
        content = self.escape_custom_tags(content)
        
        # Debug: Check code blocks after escape_custom_tags
        if self.verbose and '```' in content:
            code_blocks_after_escape = re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL)
            self.log(f"  → After escape_custom_tags: {len(code_blocks_after_escape)} code blocks")
            for idx, block in enumerate(code_blocks_after_escape):
                content_preview = block[:50] + '...' if len(block) > 50 else block
                self.log(f"    Block {idx + 1}: {repr(content_preview)}")
        
        # Clean up problematic HTML tags
        content = self.clean_html_tags(content)
        
        # Debug: Check code blocks after clean_html_tags
        if self.verbose and '```' in content:
            code_blocks_after_clean_html = re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL)
            self.log(f"  → After clean_html_tags: {len(code_blocks_after_clean_html)} code blocks")
            for idx, block in enumerate(code_blocks_after_clean_html):
                content_preview = block[:50] + '...' if len(block) > 50 else block
                self.log(f"    Block {idx + 1}: {repr(content_preview)}")
        
        # Fix MDX-specific issues
        content = self.fix_mdx_issues(content)
        
        # Fix comparison operators in tables
        content = self.fix_comparison_operators_in_tables(content)
        
        # Fix MDX parsing issues (pipe escaping, backticks, JSON arrays)
        content = self.fix_mdx_parsing_issues_ultimate(content)
        
        # Final check for inline table tags that might cause MDX issues
        # If a line contains text before a <table> tag, it's likely inline and should be escaped
        lines = content.split('\n')
        in_code_block = False
        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # Skip processing in code blocks
            if in_code_block:
                continue
                
            # Fix inline table tags
            if '<table' in line and not line.strip().startswith('<table'):
                # Find the table tag and escape it
                lines[i] = re.sub(r'<table([^>]*)>', r'`<table\1>`', line, flags=re.IGNORECASE)
            
            # Fix unescaped curly braces that cause Acorn parsing errors
            # Skip lines that look like MDX components
            if not line.strip().startswith('<'):
                # Escape JSON-like objects
                if re.search(r'\{["\'][\w\s]+["\']\s*:\s*["\'][\w\s]+["\']\}', line):
                    lines[i] = re.sub(r'(\{["\'][\w\s]+["\']\s*:\s*["\'][\w\s]+["\']\})', r'`\1`', line)
                # Escape placeholder patterns like {something}
                elif re.search(r'\{[\w\s\-_]+\}', line) and not re.search(r'<[^>]+\{[\w\s\-_]+\}[^>]*>', line):
                    lines[i] = re.sub(r'(\{[\w\s\-_]+\})', r'`\1`', line)
                # Escape variable patterns like ${something}
                if re.search(r'\$\{[\w\s\-_]+\}', line):
                    lines[i] = re.sub(r'(\$\{[\w\s\-_]+\})', r'`\1`', line)
                
                # Fix comparison operators outside of tables (but not in links or already in backticks)
                if '`' not in line and ('<' in line or '>' in line):
                    # Don't process if it looks like HTML or a link
                    if not re.search(r'<[a-zA-Z/!]|</[a-zA-Z]|[a-zA-Z]>', line) and not re.search(r'\]\([^)]+\)', line):
                        # Escape standalone comparison operators with backslashes
                        line = re.sub(r'(?<!\w)\s+<\s+(?!\w)', ' \\< ', line)
                        line = re.sub(r'(?<!\w)\s+>\s+(?!\w)', ' \\> ', line)
                        line = re.sub(r'(?<!\w)\s+<=\s+(?!\w)', ' \\<= ', line)
                        line = re.sub(r'(?<!\w)\s+>=\s+(?!\w)', ' \\>= ', line)
                        lines[i] = line
                    
        content = '\n'.join(lines)
        
        # Remove duplicate headers (if the first line is the same as a later # Header)
        lines = content.split('\n')
        if len(lines) > 1:
            first_line = lines[0].strip()
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == f'# {first_line}':
                    lines[0] = f'# {first_line}'
                    del lines[i]
                    break
        content = '\n'.join(lines)
        
        # Trim whitespace
        content = content.strip()
        
        # Final cleanup - remove any remaining /\* \*/ patterns
        # These come from MadCap Flare and get escaped by markdownify
        content = re.sub(r'^/\\\*\s*\\\*/$', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n/\\\*\s*\\\*/\n', '\n', content)
        
        # Fix escaped underscores that break MDX
        # Note: We'll do more comprehensive underscore fixing in final_mdx_cleanup
        # Here we just handle the most obvious cases
        # In heading anchors {#\_Something\_Like\_This}
        content = re.sub(r'\{#([^}]+)\}', lambda m: '{#' + m.group(1).replace('\\_', '_') + '}', content)
        
        # Debug: Count code blocks at end
        if self.verbose and '```' in content:
            code_blocks_after = len(re.findall(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL))
            self.log(f"  → clean_markdown: {code_blocks_after} code blocks at end")
        
        # Fix multiple backticks - normalize to single backticks
        # Pattern: ```text``` or ````text```` etc (but not code blocks)
        # First, handle the extreme cases with many backticks
        content = re.sub(r'`{4,}([^`]+)`{4,}', r'`\1`', content)
        
        # Fix double/triple backticks that aren't code blocks
        # Pattern: ``text`` (but not ```language at start of line)
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            # Skip lines that start code blocks
            if not line.strip().startswith('```'):
                # Replace double backticks with single
                line = re.sub(r'``([^`]+)``', r'`\1`', line)
                # Fix mismatched backticks like ``text`
                line = re.sub(r'``([^`]+)`(?!`)', r'`\1`', line)
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
        # Fix double backticks with curly braces that break MDX
        # Pattern: ``{something}` or ``{something}`\more`
        # This often happens with path placeholders
        content = re.sub(r'``\{([^}]+)\}`([^`]*)`', r'`\{\1\}\2`', content)
        # Also fix simpler case: ``text`
        content = re.sub(r'``([^`]+)`', r'`\1`', content)
        
        # Fix solo backticks and double backticks first
        content = self.fix_solo_backticks(content)
        
        # Fix curly braces - MDX interprets these as JSX expressions
        # This is a comprehensive fix for various curly brace patterns
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue
                
            # Don't process lines inside code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Fix curly braces in the line
            fixed_line = self.fix_curly_braces_in_line(line)
            fixed_lines.append(fixed_line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix incomplete code blocks - convert double backticks to triple backticks
        # This handles cases where code blocks were incorrectly marked with only two backticks
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        
        # First pass: identify and fix obvious double backtick patterns
        for i, line in enumerate(lines):
            # Track if we're in a code block
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue
            
            # Don't process lines inside code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Check if line contains exactly two backticks (standalone)
            if line.strip() == '``':
                # Look ahead to find what type of closing this needs
                found_triple_closing = False
                found_double_closing = False
                
                for j in range(i + 1, min(i + 50, len(lines))):  # Look ahead up to 50 lines
                    if lines[j].strip() == '```':
                        found_triple_closing = True
                        break
                    elif lines[j].strip() == '``':
                        found_double_closing = True
                        break
                
                # If we found a triple backtick closing ahead, this should be triple too
                if found_triple_closing and not found_double_closing:
                    fixed_lines.append(line.replace('``', '```'))
                # If we found matching double backticks, convert both to triple
                elif found_double_closing:
                    fixed_lines.append(line.replace('``', '```'))
                else:
                    # Default to triple backticks for safety
                    fixed_lines.append(line.replace('``', '```'))
            
            # Check for `` at the beginning of a line with content (like ``xml or ``json)
            elif line.strip().startswith('``') and not line.strip().startswith('```'):
                stripped = line.strip()
                # Check if it looks like ``language (common patterns)
                if len(stripped) > 2 and (
                    # Common language identifiers
                    any(stripped[2:].startswith(lang) for lang in ['json', 'xml', 'ini', 'sql', 'bash', 'python', 'javascript', 'java', 'csharp', 'yaml', 'html', 'css']) or
                    # Or starts with a letter followed by space/newline (generic language identifier)
                    (stripped[2].isalpha() and (len(stripped) == 3 or (len(stripped) > 3 and stripped[3] in ' \n')))
                ):
                    # Convert to triple backticks
                    fixed_lines.append(line.replace('``', '```', 1))
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Second pass: fix any remaining mismatched code blocks
        # Look for patterns where `` is followed by ``` (like in the supportedformats example)
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            if lines[i].strip() == '``':
                # Check if there's a ``` closing within the next ~20 lines
                found_triple = False
                for j in range(i + 1, min(i + 20, len(lines))):
                    if lines[j].strip() == '```':
                        found_triple = True
                        # Check if there's content that looks like code between them
                        has_code_content = False
                        for k in range(i + 1, j):
                            if lines[k].strip() and not lines[k].strip() == '``':
                                has_code_content = True
                                break
                        if has_code_content:
                            # This `` should be ```
                            fixed_lines.append(lines[i].replace('``', '```'))
                            i += 1
                            continue
                        break
            
            fixed_lines.append(lines[i])
            i += 1
        
        content = '\n'.join(fixed_lines)
        
        # Third pass: Fix markdownify's code block pattern
        # Markdownify sometimes creates:
        # ```
        # ``language
        # code content
        # ```
        # This should be:
        # ```language
        # code content
        # ```
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            if i + 1 < len(lines) and lines[i].strip() == '```' and lines[i + 1].strip().startswith('``'):
                # Found the pattern
                next_line = lines[i + 1].strip()
                if len(next_line) > 2 and next_line[2:].isalpha():
                    # It's a language identifier
                    lang = next_line[2:]
                    if self.verbose:
                        self.log(f"  → Found markdownify pattern: ``` followed by ``{lang}")
                    fixed_lines.append(f'```{lang}')
                    i += 2  # Skip both lines
                    continue
            
            fixed_lines.append(lines[i])
            i += 1
        
        content = '\n'.join(fixed_lines)
        
        # Remove double blank lines that might result
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Fix backticks in markdown links
        content = self.fix_backticks_in_links(content)
        
        return content
    
    def fix_backticks_in_links(self, content):
        """
        Fix markdown links that have backticks in the file paths, link text, or titles.
        
        Examples:
        - [1-`AAD_Scan` Job](`1-AAD_Scan`.md "`1-AAD_Scan` Job") 
          becomes [1-AAD_Scan Job](1-AAD_Scan.md "1-AAD_Scan Job")
        - [`Some Link`](`path/to/file`.md)
          becomes [Some Link](path/to/file.md)
        """
        # Pattern to match markdown links with potential backticks
        # Group 1: Link text (may contain backticks)
        # Group 2: URL/path (may contain backticks)
        # Group 3: Optional title (may contain backticks)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def fix_link(match):
            link_text = match.group(1)
            link_content = match.group(2)
            
            # Remove backticks from link text
            link_text = link_text.replace('`', '')
            
            # Split link content into URL and optional title
            # Title is typically after a space and in quotes (single or double)
            # First try double quotes, then single quotes
            title_match = re.match(r'([^\s"\']+)\s+"([^"]+)"', link_content)
            if not title_match:
                title_match = re.match(r"([^\s\"']+)\s+'([^']+)'", link_content)
            
            if title_match:
                # Has a title
                url = title_match.group(1)
                title = title_match.group(2)
                
                # Determine which quote type was used
                quote_char = '"' if '"' in link_content else "'"
                
                # Remove backticks from URL and title
                url = url.replace('`', '')
                title = title.replace('`', '')
                
                return f'[{link_text}]({url} {quote_char}{title}{quote_char})'
            else:
                # No title, just URL
                url = link_content.replace('`', '')
                return f'[{link_text}]({url})'
        
        # Apply the fix to all links
        content = re.sub(link_pattern, fix_link, content)
        
        return content
    
    def fix_mdx_issues(self, content):
        """Fix common patterns that break MDX parsing"""
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        in_table = False
        
        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue
                
            # Track tables
            if '|' in line and not in_code_block:
                # Simple heuristic for table detection
                if line.count('|') >= 2:
                    in_table = True
                elif in_table and line.strip() == '':
                    in_table = False
            
            # Skip processing in code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
                
            # Skip processing in tables (they often have special formatting)
            if in_table:
                fixed_lines.append(line)
                continue
            
            # Fix standalone curly braces that aren't JSON
            if line.strip() in ['{', '}'] and not self._looks_like_json_context(lines, i):
                # Escape standalone braces
                line = line.replace('{', '\\{').replace('}', '\\}')
            
            # Fix inline expressions that look like JSX
            # Pattern: {something} not in code blocks
            if '{' in line and '}' in line and not line.strip().startswith('{#'):
                # Don't escape if it's a heading anchor
                if not re.search(r'\{#[^}]+\}', line):
                    # Check if it looks like a problematic JSX expression
                    if re.search(r'\{[^}]*[<>][^}]*\}', line):
                        # Contains < or > inside braces - likely problematic
                        line = re.sub(r'(\{[^}]+\})', r'`\1`', line)
                    elif re.search(r'\{[^}]*[\[\]][^}]*\}', line):
                        # Contains [ or ] inside braces - likely problematic
                        line = re.sub(r'(\{[^}]+\})', r'`\1`', line)
                    elif re.search(r'\{[^}]*[\'"][^}]*\}', line):
                        # Contains quotes inside braces - might be problematic
                        line = re.sub(r'(\{[^}]+\})', r'`\1`', line)
            
            # Fix escaped asterisks that might cause MDX issues
            line = re.sub(r'\\\*', '*', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _looks_like_json_context(self, lines, index):
        """Check if a line with { or } is likely part of JSON"""
        # Look at surrounding lines
        start = max(0, index - 3)
        end = min(len(lines), index + 3)
        
        for i in range(start, end):
            if i == index:
                continue
            if '"' in lines[i] and ':' in lines[i]:
                return True
        return False
    
    def fix_comparison_operators_in_tables(self, content):
        """Fix unescaped comparison operators in markdown tables"""
        lines = content.split('\n')
        fixed_lines = []
        in_table = False
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue
                
            # Skip processing in code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Detect if we're in a table
            if '|' in line and line.count('|') >= 2:
                # This looks like a table row
                in_table = True
                
                # Split by pipes but preserve the structure
                parts = line.split('|')
                fixed_parts = []
                
                for i, part in enumerate(parts):
                    # Skip the first and last empty parts (from leading/trailing |)
                    if i == 0 or i == len(parts) - 1:
                        fixed_parts.append(part)
                        continue
                    
                    # Check if this cell contains comparison operators
                    # Only escape if they're standalone (with spaces around them)
                    if ' > ' in part or ' < ' in part or ' >= ' in part or ' <= ' in part:
                        # These are likely comparison operators, not HTML tags
                        part = part.replace(' > ', ' \\> ')
                        part = part.replace(' < ', ' \\< ')
                        part = part.replace(' >= ', ' \\>= ')
                        part = part.replace(' <= ', ' \\<= ')
                    
                    # Also handle cases where they're at the start/end of the cell
                    part = re.sub(r'^\s*>\s*$', ' \\> ', part)
                    part = re.sub(r'^\s*<\s*$', ' \\< ', part)
                    part = re.sub(r'^\s*>=\s*$', ' \\>= ', part)
                    part = re.sub(r'^\s*<=\s*$', ' \\<= ', part)
                    
                    fixed_parts.append(part)
                
                line = '|'.join(fixed_parts)
            elif in_table and line.strip() == '':
                # Empty line ends the table
                in_table = False
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_mdx_parsing_issues_ultimate(self, content):
        """Ultimate fix for all MDX parsing issues including the most stubborn edge cases"""
        # Debug: Check if we're processing files with Select|Execute
        if 'Select|Execute' in content or 'Select | Execute' in content:
            self.log("  → DEBUG: fix_mdx_parsing_issues_ultimate called on content with Select|Execute")
            # Pre-process the entire content to fix known problematic patterns
            # This is a failsafe for stubborn cases
            content = re.sub(r'Select\s*\|\s*Execute', r'Select\\|Execute', content)
            content = re.sub(r'Select\s*\|\s*Update', r'Select\\|Update', content)
            content = re.sub(r'Read\s*\|\s*Write', r'Read\\|Write', content)
            # Generic pattern: any letter|letter within table context
            lines_temp = content.split('\n')
            for i, line in enumerate(lines_temp):
                if '|' in line and line.count('|') >= 3:  # Likely a table row
                    # Replace letter|letter patterns in this line
                    lines_temp[i] = re.sub(r'([a-zA-Z])\|([a-zA-Z])', r'\1\\|\2', line)
            content = '\n'.join(lines_temp)
        
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        in_table = False
        code_block_delimiter = None
        
        for line_num, line in enumerate(lines):
            # Track code blocks - don't process content inside them
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                delimiter = line.strip()[:3]
                if code_block_delimiter is None:
                    code_block_delimiter = delimiter
                    in_code_block = True
                elif delimiter == code_block_delimiter:
                    code_block_delimiter = None
                    in_code_block = False
                fixed_lines.append(line)
                continue
                
            # Skip processing in code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Pre-process lines to handle specific patterns before table processing
            # Fix curly braces in non-table contexts (like GUIDs)
            if not ('|' in line and line.count('|') >= 2):
                # Fix 1: Escape ALL curly braces (not just GUIDs)
                # This catches more edge cases
                line = re.sub(r'(?<!\\)\{([^}]*)\}', r'\\{\1\\}', line)
                
                # Fix 2: Escape percent variables
                # Pattern: %variable% -> `%variable%`
                line = re.sub(r'(?<!`)%([A-Za-z0-9_\-{}]+)%(?!`)', r'`%\1%`', line)
                
                # Fix 3: Escape backslashes in paths (but not in URLs)
                # Only escape backslashes that are part of file/registry paths
                if re.search(r'\\(?![nrt\\])', line) and not re.search(r'https?://', line):
                    # Replace single backslashes with double backslashes
                    line = re.sub(r'\\(?![\\])', r'\\\\', line)
            
            # Detect if we're in a table
            if '|' in line and line.count('|') >= 2:
                in_table = True
                
                # Check if this is a table separator line (contains only -, |, and :)
                if re.match(r'^[\s\-|:]+$', line):
                    fixed_lines.append(line)
                    continue
                
                # CRITICAL FIX: Before splitting by pipes, we need to protect content in backticks
                # because backtick-enclosed content should never be split
                protected_sections = []
                protected_marker = '___PROTECTED_CONTENT_{}___ '
                
                # Find all backtick-enclosed sections and protect them
                backtick_pattern = r'`[^`]+`'
                matches = list(re.finditer(backtick_pattern, line))
                for i, match in enumerate(matches):
                    protected_sections.append(match.group())
                    line = line.replace(match.group(), protected_marker.format(i))
                
                # Split by pipes carefully to preserve content
                # Use a special marker to handle already escaped pipes
                temp_marker = '___ESCAPED_PIPE___'
                line = line.replace('\\|', temp_marker)
                parts = line.split('|')
                fixed_parts = []
                
                for i, part in enumerate(parts):
                    # Skip the first and last empty parts (from leading/trailing |)
                    if i == 0 or i == len(parts) - 1:
                        fixed_parts.append(part)
                        continue
                    
                    # Restore protected content first
                    for j, protected in enumerate(protected_sections):
                        part = part.replace(protected_marker.format(j), protected)
                    
                    # Restore temporarily replaced escaped pipes
                    part = part.replace(temp_marker, '\\|')
                    
                    # Debug logging BEFORE processing
                    if 'Select' in part and 'Execute' in part:
                        self.log(f"  → DEBUG: Found Select|Execute in part: '{part}'")
                    
                    # ULTIMATE FIX 1: Escape ALL pipes in table cells - SUPER AGGRESSIVE
                    # Specifically target letter|letter patterns as requested
                    # This will catch Select|Execute, Read|Write, etc.
                    if '|' in part:
                        original_part = part
                        # First, escape any pipe that has a letter before and after it
                        part = re.sub(r'([a-zA-Z])\|([a-zA-Z])', r'\1\\|\2', part)
                        
                        # Also catch cases where there might be spaces
                        # For example: "Select | Execute" or "Select |Execute"
                        part = re.sub(r'([a-zA-Z])\s*\|\s*([a-zA-Z])', r'\1\\|\2', part)
                        
                        # Debug: Log what we're processing if verbose
                        if 'Select' in original_part and 'Execute' in original_part:
                            self.log(f"  → DEBUG: After escaping: '{part}'")
                            self.log(f"  → DEBUG: Changed: {original_part != part}")
                    
                    # ULTIMATE FIX 2: Handle complex JSON in table cells
                    # If cell contains JSON-like content, wrap ENTIRE cell in code block
                    if ('"' in part and '{' in part) or ('"' in part and '[' in part):
                        if not (part.strip().startswith('`') and part.strip().endswith('`')):
                            part = ' `' + part.strip() + '` '
                    
                    # Fix 3: Escape ALL curly braces in table cells
                    # Don't try to be smart about GUIDs vs JSON - just escape them all
                    if '{' in part and not (part.strip().startswith('`') and part.strip().endswith('`')):
                        part = re.sub(r'(?<!\\)\{([^}]*)\}', r'\\{\1\\}', part)
                    
                    # Fix 4: Escape percent variables in table cells
                    part = re.sub(r'(?<!`)%([A-Za-z0-9_\-{}]+)%(?!`)', r'`%\1%`', part)
                    
                    # Fix 5: Handle square brackets (common in SQL/code examples)
                    # If not already in backticks, escape them
                    if '[' in part and not (part.strip().startswith('`') and part.strip().endswith('`')):
                        part = re.sub(r'\[([^\]]+)\]', r'\\[\1\\]', part)
                    
                    # Fix 6: Handle XML tags in table cells
                    if '<' in part and '>' in part:
                        if not (part.strip().startswith('`') and part.strip().endswith('`')):
                            part = re.sub(r'(<[^>]+>)', r'`\1`', part)
                    
                    # Fix 7: Escape backslashes in paths within table cells
                    if re.search(r'\\(?![nrt\\|])', part) and not re.search(r'https?://', part):
                        part = re.sub(r'\\(?![\\|])', r'\\\\', part)
                    
                    # ULTIMATE FIX 8: Handle problematic Unicode characters
                    # Replace check marks and other symbols that cause issues
                    part = part.replace('✔', '[checkmark]')
                    part = part.replace('✓', '[checkmark]')
                    part = part.replace('×', '[x]')
                    part = part.replace('✗', '[x]')
                    
                    fixed_parts.append(part)
                
                line = '|'.join(fixed_parts)
                
            elif in_table and line.strip() == '':
                # Empty line ends the table
                in_table = False
            
            # Additional fixes for non-table content
            if not in_table:
                # Fix backticks with curly braces
                line = re.sub(r'`([^`]*)`\{', r'`\1`\\{', line)
                
                # Fix XML/HTML tags outside of code blocks
                if re.search(r'<[^>]+>', line) and not line.strip().startswith('<'):
                    # Wrap inline XML/HTML tags in backticks
                    line = re.sub(r'(?<!`)<([^>]+)>(?!`)', r'`<\1>`', line)
                
                # Fix equals signs in unexpected places
                if '=' in line and not re.search(r'(href|src|class|id|style)\s*=', line):
                    # Check if it's in a link or normal HTML attribute
                    if not re.search(r'\[.*\]\(.*=.*\)', line):  # Not in markdown link
                        line = re.sub(r'(?<!["\'])\s=\s(?!["\'])', r' \\= ', line)
                
                # ULTIMATE FIX: Handle hyphens in specific contexts
                # Fix patterns like `PP-`{name} by escaping the hyphen
                line = re.sub(r'`([^`]*)-`(\s*)\{', r'`\1\\-`\2\\{', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_mdx_parsing_issues(self, content):
        """Fix specific MDX parsing issues that cause acorn errors"""
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        in_table = False
        code_block_delimiter = None
        
        for line in lines:
            # Track code blocks - don't process content inside them
            if line.strip().startswith('```') or line.strip().startswith('~~~'):
                delimiter = line.strip()[:3]
                if code_block_delimiter is None:
                    code_block_delimiter = delimiter
                    in_code_block = True
                elif delimiter == code_block_delimiter:
                    code_block_delimiter = None
                    in_code_block = False
                fixed_lines.append(line)
                continue
                
            # Skip processing in code blocks
            if in_code_block:
                fixed_lines.append(line)
                continue
            
            # Pre-process lines to handle specific patterns before table processing
            # Fix curly braces in non-table contexts (like GUIDs)
            if not ('|' in line and line.count('|') >= 2):
                # Fix 1: Escape standalone curly braces (common in GUIDs)
                # Pattern: {GUID} -> \{GUID\}
                line = re.sub(r'(?<!\\)\{([A-F0-9\-]+)\}', r'\\{\1\\}', line, flags=re.IGNORECASE)
                
                # Fix 2: Escape percent variables
                # Pattern: %variable% -> `%variable%`
                line = re.sub(r'(?<!`)%([A-Za-z0-9_\-{}]+)%(?!`)', r'`%\1%`', line)
                
                # Fix 3: Escape backslashes in paths (but not in URLs)
                # Only escape backslashes that are part of file/registry paths
                if re.search(r'\\(?![nrt\\])', line) and not re.search(r'https?://', line):
                    # Replace single backslashes with double backslashes
                    line = re.sub(r'\\(?![\\])', r'\\\\', line)
            
            # Detect if we're in a table
            if '|' in line and line.count('|') >= 2:
                in_table = True
                
                # Check if this is a table separator line (contains only -, |, and :)
                if re.match(r'^[\s\-|:]+$', line):
                    fixed_lines.append(line)
                    continue
                
                # Split by pipes carefully to preserve content
                # Use a special marker to handle already escaped pipes
                temp_marker = '___ESCAPED_PIPE___'
                line = line.replace('\\|', temp_marker)
                parts = line.split('|')
                fixed_parts = []
                
                for i, part in enumerate(parts):
                    # Skip the first and last empty parts (from leading/trailing |)
                    if i == 0 or i == len(parts) - 1:
                        fixed_parts.append(part)
                        continue
                    
                    # Restore temporarily replaced escaped pipes
                    part = part.replace(temp_marker, '\\|')
                    
                    # Fix 1: Escape pipe characters within table cells
                    # Look for patterns like "Select|Execute", "Value1|Value2", etc.
                    # Match word characters, spaces, or certain punctuation followed by pipe
                    if re.search(r'[\w)\]]\s*\|\s*[\w\[]', part):
                        # This contains patterns that should be escaped
                        part = re.sub(r'([\w)\]])\s*\|\s*([\w\[])', r'\1\\|\2', part)
                        # Handle multiple pipes in the same cell
                        while re.search(r'([\w)\]])\s*\|\s*([\w\[])', part):
                            part = re.sub(r'([\w)\]])\s*\|\s*([\w\[])', r'\1\\|\2', part)
                    
                    # Fix 2: Handle backticks with square brackets (common in SQL/JSON examples)
                    # Pattern: `[something]` needs special handling
                    # First, temporarily mark already properly formatted code
                    part = re.sub(r'`([^`]+)`', lambda m: '___CODE_START___' + m.group(1) + '___CODE_END___', part)
                    
                    # Now escape any remaining square brackets that aren't in code
                    part = re.sub(r'\[([^\]]+)\]', r'\\[\1\\]', part)
                    
                    # Restore the code blocks
                    part = part.replace('___CODE_START___', '`').replace('___CODE_END___', '`')
                    
                    # Fix 3: Escape curly braces in table cells (like GUIDs)
                    # But not if they're already escaped or part of JSON
                    if not re.search(r'\{.*:.*\}', part):  # Not JSON
                        part = re.sub(r'(?<!\\)\{([A-F0-9\-]+)\}', r'\\{\1\\}', part, flags=re.IGNORECASE)
                    
                    # Fix 4: Escape percent variables in table cells
                    part = re.sub(r'(?<!`)%([A-Za-z0-9_\-{}]+)%(?!`)', r'`%\1%`', part)
                    
                    # Fix 5: Handle complex JSON in table cells
                    # If the cell contains JSON-like content, wrap the entire cell content in backticks
                    if (re.search(r'\{"[^"]+":', part) or 
                        re.search(r'\["[^"]+"', part) or
                        re.search(r'\{.*\\\\{.*\}.*\}', part)):
                        # This looks like JSON, wrap entire content if not already wrapped
                        if not (part.strip().startswith('`') and part.strip().endswith('`')):
                            part = ' `' + part.strip() + '` '
                    
                    # Fix 6: Handle XML tags in table cells
                    if re.search(r'<[^>]+>', part):
                        # Wrap XML in backticks if not already
                        if not (part.strip().startswith('`') and part.strip().endswith('`')):
                            part = re.sub(r'(<[^>]+>)', r'`\1`', part)
                    
                    # Fix 7: Escape backslashes in paths within table cells
                    if re.search(r'\\(?![nrt\\|])', part) and not re.search(r'https?://', part):
                        part = re.sub(r'\\(?![\\|])', r'\\\\', part)
                    
                    # Fix 8: Handle special URL parameters
                    # Pattern: [dl=0] -> \[dl=0\] (but only if not in backticks)
                    if not re.search(r'`[^`]*\[[^\]]+\][^`]*`', part):
                        part = re.sub(r'(?<!\\)\[([^]]+=[^]]+)\]', r'\\[\1\\]', part)
                    
                    fixed_parts.append(part)
                
                line = '|'.join(fixed_parts)
                
            elif in_table and line.strip() == '':
                # Empty line ends the table
                in_table = False
            
            # Additional fixes for non-table content
            if not in_table:
                # Fix backticks with curly braces
                line = re.sub(r'`([^`]*)`\{', r'`\1`\\{', line)
                
                # Fix XML/HTML tags outside of code blocks
                if re.search(r'<[^>]+>', line) and not line.strip().startswith('<'):
                    # Wrap inline XML/HTML tags in backticks
                    line = re.sub(r'(?<!`)<([^>]+)>(?!`)', r'`<\1>`', line)
                
                # Fix equals signs in unexpected places (like version comparisons)
                # Pattern: "GREATER THAN 0.0.0.0" is fine, but bare = might not be
                if '=' in line and not re.search(r'(href|src|class|id|style)\s*=', line):
                    # Check if it's a comparison or assignment that needs escaping
                    line = re.sub(r'(?<!["\'])\s*=\s*(?!["\'])', r' \\= ', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def escape_custom_tags(self, content):
        """Escape custom XML/configuration tags by wrapping them in backticks or code blocks"""
        # First pass: check if we're already in a code block with XML content
        lines = content.split('\n')
        in_code_block = False
        code_block_has_xml = False
        
        for line in lines:
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_has_xml = False
                else:
                    in_code_block = False
            elif in_code_block and re.search(r'<[a-zA-Z][^>]*>', line):
                code_block_has_xml = True
        
        # If we have XML inside code blocks, don't process further
        if code_block_has_xml:
            return content
            
        # Otherwise, proceed with the original logic
        # Detect and wrap JSON/XML/Configuration blocks that aren't already in code blocks
        new_lines = []
        in_json = False
        in_xml = False
        in_config = False
        in_code_block = False
        block_lines = []
        brace_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if we're entering/exiting a code block
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
            
            # Skip processing if we're inside a code block
            if in_code_block:
                new_lines.append(line)
                continue
            
            # Check if we're starting a JSON block
            if not in_json and not in_xml and stripped == '{':
                # Look ahead to see if this looks like JSON (check next few lines)
                looks_like_json = False
                for j in range(i + 1, min(i + 4, len(lines))):
                    if '"' in lines[j] and ':' in lines[j]:
                        looks_like_json = True
                        break
                
                if looks_like_json:
                    in_json = True
                    block_lines = [line]
                    brace_count = 1
                    continue
            
            # Check if we're starting an XML/HTML block
            if not in_json and not in_xml and re.match(r'^<[a-zA-Z][^>]*>$', stripped):
                # This looks like an XML/HTML opening tag
                in_xml = True
                block_lines = [line]
                continue
            
            # Check if this looks like a configuration block
            if not in_json and not in_xml and not in_config:
                if re.match(r'^[A-Z_]+\s*=', stripped) or re.match(r'^\[[^\]]+\]$', stripped):
                    in_config = True
                    block_lines = [line]
                    continue
            
            # If we're in JSON, track braces
            if in_json:
                block_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                
                # End of JSON block
                if brace_count == 0:
                    # Wrap in code block
                    new_lines.append('```json')
                    new_lines.extend(block_lines)
                    new_lines.append('```')
                    in_json = False
                    block_lines = []
                    brace_count = 0
                continue
            
            # If we're in XML, look for closing
            if in_xml:
                block_lines.append(line)
                # Simple heuristic: empty line ends XML block
                if stripped == '' or (i + 1 < len(lines) and not lines[i + 1].strip().startswith('<')):
                    new_lines.append('```xml')
                    new_lines.extend(block_lines[:-1] if stripped == '' else block_lines)
                    new_lines.append('```')
                    if stripped == '':
                        new_lines.append('')
                    in_xml = False
                    block_lines = []
                continue
            
            # If we're in config, look for end
            if in_config:
                if re.match(r'^[A-Z_]+\s*=', stripped) or re.match(r'^\[[^\]]+\]$', stripped):
                    block_lines.append(line)
                else:
                    # End of config block
                    new_lines.append('```ini')
                    new_lines.extend(block_lines)
                    new_lines.append('```')
                    new_lines.append(line)
                    in_config = False
                    block_lines = []
                continue
            
            new_lines.append(line)
        
        # Handle unclosed blocks
        if block_lines:
            if in_json:
                new_lines.append('```json')
            elif in_xml:
                new_lines.append('```xml')
            elif in_config:
                new_lines.append('```ini')
            new_lines.extend(block_lines)
            new_lines.append('```')
        
        content = '\n'.join(new_lines)
        
        # First, escape placeholder patterns like [<table name>] that might be confused with HTML
        content = re.sub(r'\[<([^>]+)>\]', r'[`<\1>`]', content)
        
        # Also handle cases where <table name> appears without brackets
        content = re.sub(r'(?<!\[)<(table\s+name)>(?!\])', r'`<\1>`', content, flags=re.IGNORECASE)
        
        
        # List of tags that are clearly configuration/custom tags from your report
        custom_tags = {
            'entry', 'accesscontrolrule', 'property', 'control', 'connectionidentifier',
            'filter', 'commonparameters', 'maincontrol', 'taskentitytype', 'pointcut',
            'entitytype', 'pscredential', 'recordcontrol', 'customclaimsprincipal',
            'displayentitytype', 'activity', 'job', 'displaytable', 'menuitem',
            'workflow', 'taskdependsontask', 'recorduniqueitemcontrol', 'taskresourcetype',
            'connection', 'recordsection', 'fulfilltask', 'entityassociation',
            'homonymentitylink', 'identifier', 'scalarrule', 'universe', 'resourcetype',
            'openidclient', 'exporttask', 'organization', 'entityassociationmapping',
            'entitypropertyexpression', 'connector', 'computerolemodeltask',
            'computecorrelationkeystask', 'generateprovisioningorderstask',
            'universedatamodel', 'domain', 'profile', 'contextrule', 'synchronizetask',
            'entityinstance', 'notificationaspect', 'recipient', 'entitytypemapping',
            'configurationfile', 'dimension', 'preparesynchronizationtask',
            'updateentitypropertyexpressionstask', 'builduniquevalueaspect',
            'navigationrule', 'int32', 'component', 'password', 'workfloweditentityform',
            'recordsummarycontrol', 'actionpreference', 'addchangeaspect'
        }
        
        
        # Process line by line
        lines = content.split('\n')
        new_lines = []
        in_config_block = False
        config_lines = []
        
        for line in lines:
            # Check if this line contains custom tags
            has_custom_tag = False
            for tag in custom_tags:
                if f'<{tag}' in line.lower() or f'</{tag}>' in line.lower():
                    has_custom_tag = True
                    break
            
            if has_custom_tag:
                # For inline tags, wrap in backticks
                if line.strip().startswith('-') or line.strip().startswith('*') or line.strip().startswith('>'):
                    # It's in a list or quote, escape inline
                    line = re.sub(r'<([^>]+)>', r'`<\1>`', line)
                    new_lines.append(line)
                else:
                    # Start or continue a code block
                    if not in_config_block:
                        in_config_block = True
                        if new_lines and new_lines[-1].strip():
                            new_lines.append('')  # Add blank line before code block
                        new_lines.append('```xml')
                    new_lines.append(line)
            else:
                # Not a config line
                if in_config_block:
                    # Close the code block
                    new_lines.append('```')
                    if line.strip():
                        new_lines.append('')  # Add blank line after code block
                    in_config_block = False
                new_lines.append(line)
        
        # Close any remaining code block
        if in_config_block:
            new_lines.append('```')
        
        return '\n'.join(new_lines)
    
    def clean_html_tags(self, content):
        """Clean up problematic HTML tags in markdown"""
        # First, handle inline table tags that appear within sentences/paragraphs
        # These are often placeholders rather than actual HTML tables
        lines = content.split('\n')
        new_lines = []
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
            
            # Skip processing in code blocks
            if in_code_block:
                new_lines.append(line)
                continue
                
            # Check if this line has a table tag but is not actually a table structure
            if '<table' in line.lower() and not line.strip().startswith('<table'):
                # This is likely an inline reference, escape it
                line = re.sub(r'<table([^>]*)>', r'`<table\1>`', line, flags=re.IGNORECASE)
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Remove self-closing slashes from void elements
        void_elements = ['br', 'hr', 'img', 'input', 'meta', 'area', 'base', 'col', 'embed', 'link', 'param', 'source', 'track', 'wbr']
        for elem in void_elements:
            # Fix self-closing tags like <br/> to <br>
            content = re.sub(rf'<{elem}\s*/>', f'<{elem}>', content, flags=re.IGNORECASE)
            # Fix tags with attributes like <br class="foo"/> to <br class="foo">
            content = re.sub(rf'<{elem}(\s+[^>]*?)/>', rf'<{elem}\1>', content, flags=re.IGNORECASE)
        
        # Convert <br> tags to markdown line breaks
        content = re.sub(r'<br\s*/?>', '  \n', content, flags=re.IGNORECASE)
        
        # Remove empty paragraphs
        content = re.sub(r'<p>\s*</p>', '', content, flags=re.IGNORECASE)
        
        # Fix unclosed table elements
        # Tables are tricky - if we have unclosed table tags, it's often better to remove the whole table
        lines = content.split('\n')
        fixed_lines = []
        in_table = False
        table_tag_count = {'table': 0, 'tbody': 0, 'tr': 0, 'td': 0, 'th': 0}
        
        for i, line in enumerate(lines):
            # Count opening tags
            for tag in table_tag_count:
                table_tag_count[tag] += len(re.findall(rf'<{tag}[^>]*>', line, re.IGNORECASE))
                table_tag_count[tag] -= len(re.findall(rf'</{tag}>', line, re.IGNORECASE))
            
            # Check if we're in a table
            if table_tag_count['table'] > 0:
                in_table = True
            
            # If we exit a table, check if tags were balanced
            if in_table and table_tag_count['table'] == 0:
                in_table = False
                # Reset all table-related counts
                for tag in table_tag_count:
                    if table_tag_count[tag] != 0:
                        # Unbalanced table, add closing tags
                        if table_tag_count['td'] > 0:
                            line += '</td>' * table_tag_count['td']
                        if table_tag_count['tr'] > 0:
                            line += '</tr>' * table_tag_count['tr']
                        if table_tag_count['tbody'] > 0:
                            line += '</tbody>' * table_tag_count['tbody']
                        table_tag_count[tag] = 0
            
            fixed_lines.append(line)
        
        # If we ended while still in a table, close it
        if sum(table_tag_count.values()) > 0:
            closing_tags = []
            if table_tag_count['td'] > 0:
                closing_tags.append('</td>' * table_tag_count['td'])
            if table_tag_count['tr'] > 0:
                closing_tags.append('</tr>' * table_tag_count['tr'])
            if table_tag_count['tbody'] > 0:
                closing_tags.append('</tbody>' * table_tag_count['tbody'])
            if table_tag_count['table'] > 0:
                closing_tags.append('</table>' * table_tag_count['table'])
            if closing_tags:
                fixed_lines.append(''.join(closing_tags))
        
        content = '\n'.join(fixed_lines)
        
        # Fix unclosed <a> tags
        content = re.sub(r'<a\s+[^>]*>([^<]*?)(?=\n\n|$)', r'<a>\1</a>', content, flags=re.IGNORECASE)
        
        # Fix unclosed <b> tags
        content = re.sub(r'<b>([^<]*?)(?=\n\n|$)', r'<b>\1</b>', content, flags=re.IGNORECASE)
        
        # Fix unclosed <h1> tags (and other headers)
        for i in range(1, 7):
            content = re.sub(rf'<h{i}>([^<\n]*?)$', rf'<h{i}>\1</h{i}>', content, flags=re.IGNORECASE | re.MULTILINE)
        
        # Try to fix unclosed tags by removing problematic ones
        # Remove unclosed spans, divs, and other inline elements
        problematic_tags = ['span', 'div', 'font', 'center', 'small', 'big', 'sup', 'sub', 'p']
        for tag in problematic_tags:
            # Remove orphaned closing tags
            content = re.sub(rf'</{tag}>\s*\n', '\n', content, flags=re.IGNORECASE)
            # Remove unclosed opening tags at end of paragraphs
            content = re.sub(rf'<{tag}[^>]*>([^<]*?)(\n\n|$)', r'\1\2', content, flags=re.IGNORECASE)
        
        # Process content line by line to protect code blocks
        lines = content.split('\n')
        new_lines = []
        in_code_block = False
        
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
            
            # Skip processing in code blocks
            if in_code_block:
                new_lines.append(line)
                continue
            
            # Clean up orphaned closing tags (but only outside code blocks)
            # Handle multiple closing tags in a row like </tr></tr></tr>
            line = re.sub(r'(</\w+>\s*)+$', '', line)
            # Also clean up orphaned closing tags at start of lines
            line = re.sub(r'^(</\w+>\s*)+', '', line)
            
            # Remove problematic tags from this line
            line = re.sub(r'<(?!/?(?:a|img|code|pre|ul|ol|li|table|tr|td|th|thead|tbody|strong|em|b|i|blockquote|h[1-6])\b)[^>]+>', '', line, flags=re.IGNORECASE)
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        return content
    
    def final_mdx_cleanup(self, content):
        """Final cleanup pass specifically for MDX/Docusaurus compatibility"""
        if not self.docusaurus:
            return content
        
        lines = content.split('\n')
        cleaned_lines = []
        in_frontmatter = False
        frontmatter_count = 0
        
        for line in lines:
            # Track frontmatter section
            if line.strip() == '---':
                frontmatter_count += 1
                in_frontmatter = frontmatter_count == 1
                cleaned_lines.append(line)
                continue
            
            # Don't process frontmatter content
            if in_frontmatter:
                cleaned_lines.append(line)
                continue
            # Fix all escaped underscores - they break MDX
            # But skip headings as they might need exact text matching for anchors
            if not line.strip().startswith('#') and not line.strip().startswith('<h'):
                line = line.replace('\\_', '_')
            
            # Fix escaped asterisks
            line = line.replace('\\*', '*')
            
            # Fix (Optional) at start of list items - wrap in backticks
            line = re.sub(r'^(\s*-\s*)\(Optional\)', r'\1`(Optional)`', line)
            
            # Fix @ symbols in inline text (common for parameter names)
            # Don't touch @ in code blocks or already in backticks
            if not line.strip().startswith('```') and '`' not in line:
                # Replace @word patterns with backticks
                line = re.sub(r'@(\w+)', r'`@\1`', line)
            
            # Fix identifiers with underscores - these break MDX
            # Common patterns:
            # - Table names: SA_EX_TableName
            # - File system operations: fs_DeleteFiles
            # - Job names: 0-SQL_InstanceDiscovery
            # - Prefixed identifiers: FS_Something, AD_Something, SP_Something
            
            # Skip processing headings - we don't want backticks in heading text
            if line.strip().startswith('#'):
                cleaned_lines.append(line)
                continue
            
            # Don't process if line already has backticks around these patterns
            # Also skip if we're inside a markdown link [text](url)
            if not re.search(r'`[^`]*(SA_|EX_|FS_|AD_|SP_|fs_|ad_|sp_|ex_)', line):
                # Protect entire markdown links (including text, URL, and title)
                link_placeholder = "<<<PROTECTED_LINK_>>>"
                link_counter = 0
                link_map = {}
                
                # Find all markdown links and replace them temporarily
                def replace_link(match):
                    nonlocal link_counter
                    link_id = f"{link_placeholder}{link_counter}"
                    link_map[link_id] = match.group(0)  # Store the entire link
                    link_counter += 1
                    return link_id
                
                # Match links with optional title: [text](url) or [text](url "title")
                line = re.sub(r'\[[^\]]+\]\([^)]+\)', replace_link, line)
                
                # Now apply the identifier fixes (only outside of links)
                # Table and system identifiers
                line = re.sub(r'\b((?:SA|EX|FS|AD|SP|NIS|SG|AAD|AWS|DB)_[A-Za-z0-9_]+)\b', r'`\1`', line)
                # Lowercase versions
                line = re.sub(r'\b((?:fs|ad|sp|ex|nis|sg|aad|aws|db)_[A-Za-z0-9_]+)\b', r'`\1`', line)
                
                # Restore the original links
                for link_id, link_content in link_map.items():
                    line = line.replace(link_id, link_content)
            
            # Job names with numbers and underscores (e.g., 0-SQL_InstanceDiscovery)
            # Protect links first
            link_placeholder = "<<<PROTECTED_LINK2_>>>"
            link_counter = 0
            link_map = {}
            
            def replace_link(match):
                nonlocal link_counter
                link_id = f"{link_placeholder}{link_counter}"
                link_map[link_id] = match.group(0)
                link_counter += 1
                return link_id
            
            # Protect all links
            line = re.sub(r'\[[^\]]+\]\([^)]+\)', replace_link, line)
            
            # Apply the pattern only outside of links
            line = re.sub(r'\b(\d+-[A-Z]+_[A-Za-z0-9_]+)\b', r'`\1`', line)
            
            # Restore links
            for link_id, link_content in link_map.items():
                line = line.replace(link_id, link_content)
            
            # Fix numbered list items with special formatting
            # e.g., "00. Deletes all Stored Data - LEAVE UNCHECKED"
            line = re.sub(r'^(\s*-?\s*\d+\.\s+[^-]+)\s*-\s*LEAVE\s+(UNCHECKED|CHECKED)', 
                         r'\1 - **LEAVE \2**', line)
            
            # Fix escaped pipes in tables (common issue)
            if '|' in line and line.count('|') >= 2:
                # This might be a table row
                line = line.replace('\\|', '|')
            
            # Fix escaped brackets
            line = line.replace('\\[', '[').replace('\\]', ']')
            
            # Fix escaped parentheses in non-link contexts
            if not re.search(r'\]\([^)]+\)', line):
                line = line.replace('\\(', '(').replace('\\)', ')')
            
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Fix heading anchors with escaped characters
        content = re.sub(r'\{#([^}]+)\}', lambda m: '{#' + m.group(1).replace('\\', '') + '}', content)
        
        # Fix link text with escaped underscores
        # Match [text with_underscores](url)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', 
                        lambda m: '[' + m.group(1).replace('\\_', '_') + '](' + m.group(2) + ')', 
                        content)
        
        # Ensure proper spacing around headings
        content = re.sub(r'(^|\n)(#{1,6})\s*([^\n]+)', r'\1\2 \3', content, flags=re.MULTILINE)
        
        return content
    
    def add_docusaurus_frontmatter(self, content, html_file):
        """Add Docusaurus-compatible frontmatter to the markdown"""
        # Extract the title from the content
        lines = content.split('\n')
        title = None
        title_index = None
        
        # Look for the first heading
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
                title_index = i
                # Remove any heading anchor from the title
                # e.g., "Getting Started {#GettingStartedWithStealthAUDIT}" -> "Getting Started"
                title = re.sub(r'\s*\{#[^}]+\}$', '', title)
                # Remove backticks that markdownify might have added
                title = title.replace('`', '')
                break
        
        # If no heading found, use filename
        if not title:
            title = html_file.stem.replace('_', ' ').replace('-', ' ').title()
        
        # Remove escaped underscores from title (these break MDX)
        title = title.replace('\\_', '_')
        
        # Remove backticks from title (they cause YAML parsing issues)
        title = title.replace('`', '')
        
        # Check if there's a duplicate title line before the heading
        # This often happens with navigation/breadcrumb elements
        if title_index is not None and title_index > 0:
            # Check the line before the heading
            prev_line = lines[title_index - 1].strip()
            if prev_line and prev_line.replace('`', '') == title:
                # Remove the duplicate title line
                lines.pop(title_index - 1)
                content = '\n'.join(lines)
        
        # Generate a simple ID from the filename
        doc_id = html_file.stem.lower().replace(' ', '-').replace('_', '-')
        
        # Create frontmatter - properly escape title for YAML
        # YAML requires quotes for values containing special characters
        # Note: In YAML, & is NOT a special character within quoted strings
        if any(char in title for char in [':', '"', "'", '|', '>', '-', '?', '@', '`', '!', '#', '$', '%', '^', '&', '*', '=', '[', ']', '{', '}', '\\', ';', '\n']):
            # Prefer single quotes for simplicity (only need to escape single quotes)
            if "'" in title and '"' not in title:
                # Use double quotes if title contains single quotes but not double quotes
                # Only escape backslashes, double quotes, and newlines (NOT ampersands)
                title_escaped = title.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                title_value = f'"{title_escaped}"'
            elif "'" in title and '"' in title:
                # Both quote types present - use double quotes and escape properly
                title_escaped = title.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                title_value = f'"{title_escaped}"'
            else:
                # Use single quotes (simpler - only need to escape single quotes)
                # Ampersands are fine in YAML quoted strings
                title_escaped = title.replace("'", "''")
                title_value = f"'{title_escaped}'"
        else:
            title_value = title
            
        frontmatter = f"""---
id: {doc_id}
title: {title_value}
---

"""
        
        # Add frontmatter to content
        return frontmatter + content


def main():
    parser = argparse.ArgumentParser(
        description='Convert HTML documentation to Markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python convert_docs.py ./html_docs ./markdown_output
  python convert_docs.py ./html_docs ./markdown_output --verbose
  python convert_docs.py ./html_docs ./markdown_output --docusaurus --lowercase
        '''
    )
    
    parser.add_argument('input_dir', help='Input directory containing HTML files')
    parser.add_argument('output_dir', help='Output directory for Markdown files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--list-files', action='store_true', help='List all files found before converting')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be converted without actually converting')
    parser.add_argument('--find-image', type=str, help='Find where a specific image is referenced (provide image filename)')
    parser.add_argument('--flatten', action='store_true', help='Remove redundant nested directories (e.g., PolicyPak/PolicyPak -> PolicyPak)')
    parser.add_argument('--docusaurus', action='store_true', help='Add Docusaurus-compatible frontmatter and clean navigation elements')
    parser.add_argument('--lowercase', action='store_true', help='Convert all file and directory names to lowercase (recommended for Docusaurus)')
    parser.add_argument('--test-mdx', action='store_true', help='Run MDX validation after conversion')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return 1
        
    # Handle find-image flag
    if args.find_image:
        converter = HTMLToMarkdownConverter(args.input_dir, args.output_dir, args.verbose, args.flatten, args.docusaurus, args.lowercase)
        converter.find_image_references(args.find_image)
        return 0
    
    # Create converter and run
    converter = HTMLToMarkdownConverter(args.input_dir, args.output_dir, args.verbose, args.flatten, args.docusaurus, args.lowercase)
    
    # Add dry_run attribute if specified
    if args.dry_run:
        converter.dry_run = True
        print("DRY RUN MODE - No files will be created\n")
    
    # List all files if requested
    if args.list_files or args.dry_run:
        print("\nSearching for HTML files...")
        all_files = list(Path(args.input_dir).rglob('*'))
        html_extensions = {'.html', '.htm', '.xhtml', '.xhtm'}
        
        html_files = [f for f in all_files if f.suffix.lower() in html_extensions]
        other_files = [f for f in all_files if f.is_file() and f.suffix.lower() not in html_extensions]
        
        print(f"\nFound {len(html_files)} HTML files:")
        for f in sorted(html_files)[:20]:  # Show first 20
            print(f"  - {f.relative_to(args.input_dir)}")
        if len(html_files) > 20:
            print(f"  ... and {len(html_files) - 20} more")
            
        print(f"\nFound {len(other_files)} non-HTML files")
        
        # Show file type distribution
        from collections import Counter
        extensions = Counter(f.suffix.lower() for f in all_files if f.is_file())
        print("\nFile types in directory:")
        for ext, count in extensions.most_common(10):
            print(f"  {ext or '(no extension)'}: {count} files")
        
        if args.dry_run:
            return 0
    
    converter.convert()
    
    # Run MDX validation if requested
    if args.test_mdx:
        print("\nRunning MDX validation...")
        import subprocess
        try:
            result = subprocess.run(['node', 'mdx-test-suite.js', args.output_dir], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ All files passed MDX validation")
            else:
                print("✗ MDX validation found errors")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
        except FileNotFoundError:
            print("⚠ MDX test suite not found. Make sure mdx-test-suite.js is in the current directory")
    
    return 0


if __name__ == '__main__':
    exit(main())