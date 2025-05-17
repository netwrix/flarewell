"""
Link mapping utility for converting Flare references to Docusaurus paths.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from urllib.parse import urljoin, urlparse

class LinkMapper:
    """
    Maps Flare links to Docusaurus paths.
    
    This utility handles:
    - Building a registry of all content files
    - Normalizing relative paths
    - Converting links based on the new file structure
    """
    
    def __init__(self, preserve_structure: bool = True, debug: bool = False):
        """
        Initialize the link mapper.
        
        Args:
            preserve_structure: Whether to maintain original file structure
            debug: Enable debug logging
        """
        self.preserve_structure = preserve_structure
        self.debug = debug
        self.link_map: Dict[str, str] = {}
        self.file_registry: Dict[str, Dict[str, Any]] = {}
        self.processed_files: Set[str] = set()
        
        # Configure logging
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("LinkMapper")
    
    def register_file(self, file_info: Dict[str, Any]) -> None:
        """
        Register a file in the mapping registry.
        
        Args:
            file_info: Dictionary with file information including original and new paths
        """
        original_path = file_info.get("rel_path", "")
        if not original_path:
            return
        
        # Normalize path (handle case sensitivity, ensure proper slashes)
        norm_orig_path = self._normalize_path(original_path)
        
        # Determine target path
        if self.preserve_structure:
            # Just change extension
            target_path = os.path.splitext(norm_orig_path)[0]
        else:
            # Use the new path if provided
            target_path = file_info.get("new_path", norm_orig_path)
            if target_path.endswith((".htm", ".html")):
                target_path = os.path.splitext(target_path)[0]
        
        # Store in registry with normalized paths
        self.file_registry[norm_orig_path] = {
            "original_path": original_path,
            "target_path": target_path,
            "title": file_info.get("title", ""),
        }
        
        # Add to link map (with and without extension)
        self.link_map[norm_orig_path] = target_path
        
        # Also register the path without extension
        base_path = os.path.splitext(norm_orig_path)[0]
        self.link_map[base_path] = target_path
        
        # And handle common variations
        for ext in [".htm", ".html"]:
            self.link_map[base_path + ext] = target_path
            
            # Add lowercased version for case-insensitive matching
            self.link_map[base_path.lower() + ext] = target_path
            self.link_map[(base_path + ext).lower()] = target_path
        
        # Add lowercased version for case-insensitive matching
        self.link_map[norm_orig_path.lower()] = target_path
        self.link_map[base_path.lower()] = target_path
        
        if self.debug:
            self.logger.debug(f"Registered file: {norm_orig_path} → {target_path}")
    
    def register_files(self, file_list: List[Dict[str, Any]]) -> None:
        """
        Register multiple files at once.
        
        Args:
            file_list: List of file info dictionaries
        """
        for file_info in file_list:
            self.register_file(file_info)
        
        if self.debug:
            self.logger.debug(f"Registered {len(file_list)} files. Link map now contains {len(self.link_map)} entries.")
            # Log a sample of the link map for debugging
            sample_entries = list(self.link_map.items())[:5]
            for key, value in sample_entries:
                self.logger.debug(f"Link map entry: {key} → {value}")
    
    def transform_links(self, content: str, current_file_path: str) -> str:
        """
        Transform all links in content relative to the current file.
        
        Args:
            content: Markdown content with links to transform
            current_file_path: Path of the current file being processed
            
        Returns:
            Content with links transformed to match Docusaurus structure
        """
        self.processed_files.add(current_file_path)
        
        # Pattern for Markdown links and HTML links 
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\s*(?:"[^"]*")?\)'
        html_link_pattern = r'<a\s+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        
        # Get normalized base path for current file
        current_dir = os.path.dirname(self._normalize_path(current_file_path))
        
        if self.debug:
            self.logger.debug(f"Processing links in: {current_file_path}")
            self.logger.debug(f"Current directory context: {current_dir}")
        
        # Process Markdown links
        def transform_md_link(match):
            text = match.group(1)
            link = match.group(2)
            
            # Extract title if present
            title_match = re.search(r'\s+"([^"]+)"$', link)
            title = ""
            if title_match:
                title = f' "{title_match.group(1)}"'
                link = link.replace(title_match.group(0), '')
            
            new_link = self._resolve_link(link, current_dir)
            
            if self.debug:
                self.logger.debug(f"MD Link: '{link}' → '{new_link}'")
                
            return f"[{text}]({new_link}{title})"
        
        content = re.sub(md_link_pattern, transform_md_link, content)
        
        # Process HTML links
        def transform_html_link(match):
            link = match.group(1)
            text = match.group(2)
            new_link = self._resolve_link(link, current_dir)
            
            if self.debug:
                self.logger.debug(f"HTML Link: '{link}' → '{new_link}'")
                
            return f"[{text}]({new_link})"
        
        content = re.sub(html_link_pattern, transform_html_link, content)
        
        return content
    
    def _resolve_link(self, link: str, current_dir: str) -> str:
        """
        Resolve a link path to its target in the new structure.
        
        Args:
            link: Original link path
            current_dir: Directory of the file containing the link
            
        Returns:
            Resolved link path
        """
        # Skip external links or anchors
        if link.startswith(('http://', 'https://', 'mailto:', '#')):
            return link
        
        # Handle anchors in internal links
        link_parts = link.split('#', 1)
        path = link_parts[0]
        anchor = link_parts[1] if len(link_parts) > 1 else ''
        
        # If there's no path (just an anchor), return as is
        if not path:
            return f"#{anchor}" if anchor else ""
            
        # Normalize and resolve the path relative to current file
        norm_path = self._normalize_path(path)
        
        # Handle relative paths
        if not norm_path.startswith('/'):
            # Join with the current directory to get absolute path
            abs_path = os.path.normpath(os.path.join(current_dir, norm_path))
            norm_path = self._normalize_path(abs_path)
        else:
            # Remove leading slash for lookup
            norm_path = norm_path.lstrip('/')
        
        if self.debug:
            self.logger.debug(f"Resolving link: '{path}' from context '{current_dir}'")
            self.logger.debug(f"Normalized path: '{norm_path}'")
            
        # Try both case-sensitive and case-insensitive lookups with different variations
        target = None
        variants_to_try = [
            # Exact path with extension
            norm_path,
            # Lowercase with extension
            norm_path.lower(),
            # Without extension
            os.path.splitext(norm_path)[0],
            # Lowercase without extension
            os.path.splitext(norm_path)[0].lower(),
        ]
        
        # Add extension variations
        base_path = os.path.splitext(norm_path)[0]
        for ext in ['.htm', '.html']:
            variants_to_try.append(base_path + ext)
            variants_to_try.append((base_path + ext).lower())
        
        # Try all variants
        for variant in variants_to_try:
            if variant in self.link_map:
                target = self.link_map[variant]
                if self.debug:
                    self.logger.debug(f"Found match with variant: '{variant}'")
                break
        
        # If no match found in link map
        if target is None:
            # Just strip extension as fallback
            if path.endswith(('.htm', '.html')):
                target = os.path.splitext(norm_path)[0]
            else:
                target = norm_path
            
            if self.debug:
                self.logger.debug(f"No match found in link map, using fallback: '{target}'")
        
        # If we're preserving structure, ensure we get a relative path correctly
        if self.preserve_structure and current_dir:
            if not os.path.isabs(target):
                # Make sure we're working with an absolute path for relpath calculation
                if not target.startswith('/'):
                    # Calculate relative path from current file to target
                    target_dir = os.path.dirname(target)
                    target_file = os.path.basename(target)
                    
                    if current_dir == target_dir:
                        # Same directory
                        target = target_file
                    else:
                        try:
                            # Calculate relative path
                            rel_path = os.path.relpath(target, current_dir).replace('\\', '/')
                            
                            # For root level links, don't use "./" prefix
                            if rel_path.startswith('./') and '/' not in rel_path[2:]:
                                rel_path = rel_path[2:]
                                
                            target = rel_path
                        except ValueError:
                            # If relpath fails (e.g., cross-device), keep target as is
                            pass
        
        # Add anchor if it existed
        if anchor:
            target = f"{target}#{anchor}"
        
        if self.debug:
            self.logger.debug(f"Resolved to: '{target}'")
            
        return target
    
    def _normalize_path(self, path: str) -> str:
        """
        Normalize a path for consistent comparisons.
        
        Args:
            path: File path to normalize
            
        Returns:
            Normalized path
        """
        # Normalize slashes to forward slashes
        norm_path = path.replace('\\', '/')
        
        # Remove leading/trailing slashes and whitespace
        norm_path = norm_path.strip().strip('/')
        
        # Remove duplicate slashes
        norm_path = re.sub(r'/+', '/', norm_path)
        
        return norm_path
    
    def get_unresolved_links(self) -> List[Dict[str, Any]]:
        """
        Get a list of links that could not be resolved.
        
        Returns:
            List of unresolved link information
        """
        # Future implementation to track broken links
        return []
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a report on link mapping status.
        
        Returns:
            Dictionary with link mapping statistics
        """
        return {
            "total_files": len(self.file_registry),
            "processed_files": len(self.processed_files),
            "total_links": len(self.link_map),
        }
    
    def dump_link_map(self, limit: int = 20) -> None:
        """
        Dump the link map to the log for debugging.
        
        Args:
            limit: Maximum number of entries to display
        """
        sorted_entries = sorted(self.link_map.items())
        for i, (key, value) in enumerate(sorted_entries):
            if i >= limit:
                self.logger.debug(f"... and {len(sorted_entries) - limit} more entries")
                break
            self.logger.debug(f"Link map entry {i+1}: {key} → {value}") 