"""
Core conversion functionality for Flarewell.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


from flarewell.flare_parser import FlareHtmlParser
from flarewell.docusaurus_formatter import DocusaurusFormatter
from flarewell.link_mapper import LinkMapper
from flarewell.markdown_image_cleaner import MarkdownImageCleaner


class FlareConverter:
    """Convert Flare content to Markdown."""

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        preserve_structure: bool = True,
        generate_sidebars: bool = True,
        exclude_dirs: Optional[List[str]] = None,
        debug: bool = False,
        markdown_style: str = "docusaurus",
    ):
        """Create a converter.

        Args:
            input_dir: Source directory containing Flare HTML or project files.
            output_dir: Directory for the generated Markdown files.
            input_type: Either ``"project"`` or ``"html"``.
            preserve_structure: Mirror the input directory structure in the
                output directory.
            generate_sidebars: Generate ``sidebars.js`` in the output.
            target: Optional Flare target to build from.
            exclude_dirs: Directories to exclude from conversion.
            debug: Enable verbose logging.
            markdown_style: ``"docusaurus"`` or ``"markdown"``.
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.preserve_structure = preserve_structure
        self.generate_sidebars = generate_sidebars
        self.exclude_dirs = exclude_dirs or []
        self.debug = debug
        self.markdown_style = markdown_style
        
        # Initialize counters
        self.stats = {
            "converted": 0,
            "skipped": 0,
            "errors": 0,
        }
        
        # Initialize the parser for Flare HTML output
        self.parser = FlareHtmlParser(self.input_dir)
        
        # Initialize link mapper
        self.link_mapper = LinkMapper(preserve_structure=self.preserve_structure, debug=self.debug)
        
        # Initialize the formatter
        self.formatter = DocusaurusFormatter(
            link_mapper=self.link_mapper,
            general_markdown=(self.markdown_style != "docusaurus"),
        )

        # Directory for relocated images
        self.static_img_dir = self.output_dir.parent / "static" / "img"
        self.image_map: Dict[Path, Path] = {}
        

    def convert(self) -> Dict[str, int]:
        """
        Main conversion process.
        
        Returns:
            Dict with conversion statistics.
        """
        # Parse the Flare HTML structure
        project_structure = self.parser.parse()
        
        # Filter topics based on exclude_dirs if specified
        if self.exclude_dirs:
            filtered_topics = []
            for item in project_structure.get("topics", []):
                rel_path = item.get("rel_path", "")
                exclude = False
                for exclude_dir in self.exclude_dirs:
                    if exclude_dir in rel_path:
                        exclude = True
                        self.stats["skipped"] += 1
                        break
                if not exclude:
                    filtered_topics.append(item)
            project_structure["topics"] = filtered_topics
        
        # First, build the complete link mapping registry
        print("Building link mapping registry...")
        self.link_mapper.register_files(project_structure.get("topics", []))
        
        # Dump the link map for debugging if requested
        if self.debug:
            self.link_mapper.dump_link_map()
        
        # Process files
        file_count = len(project_structure.get("topics", []))
        print(f"Converting {file_count} files...")
        
        for i, item in enumerate(project_structure.get("topics", [])):
            try:
                # Print progress indicator for large projects
                if file_count > 100 and i % 100 == 0:
                    print(f"Progress: {i}/{file_count} files ({i/file_count*100:.1f}%)")
                
                self._process_file(item)
                self.stats["converted"] += 1
            except Exception as e:
                print(f"Error processing {item.get('path')}: {str(e)}")
                self.stats["errors"] += 1
        
        # Copy non-image assets
        self._copy_assets(project_structure.get("assets", []))

        # Relocate tracked images
        self._copy_tracked_images()
        
        # Generate sidebar.js if requested
        if self.generate_sidebars:
            self._generate_sidebar(project_structure)
        
        # Print link mapping report
        link_report = self.link_mapper.generate_report()
        print(f"Link mapping: {link_report['total_files']} files registered, "
              f"{link_report['total_links']} links mapped, "
              f"{link_report['processed_files']} files processed")

        return self.stats
    
    def _process_file(self, file_info: Dict[str, Any]) -> None:
        """
        Process a single file, converting it to Markdown and writing to the output dir.
        
        Args:
            file_info: Dictionary with file information.
        """
        content = self.parser.get_content(file_info)

        # Determine output path
        if self.preserve_structure:
            rel_path = file_info.get("rel_path", file_info.get("path", ""))
            output_path = self.output_dir / rel_path
        else:
            output_path = self.output_dir / file_info.get("new_path", file_info.get("rel_path", ""))

        output_path = output_path.with_suffix(".md")

        images = content.get("images", [])

        # Convert to markdown
        md_content = self.formatter.to_markdown(content)

        for img in images:
            new_ref = self._register_image(img, file_info, output_path)
            if new_ref:
                md_content = md_content.replace(img, new_ref)
        
        # Add front matter
        md_content = self.formatter.add_frontmatter(
            md_content, 
            title=file_info.get("title", ""),
            sidebar_position=file_info.get("position", 1),
            description=file_info.get("description", ""),
        )
        
        
        # Create directories if they don't exist
        os.makedirs(output_path.parent, exist_ok=True)
        
        # Write the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        if self.debug and "rel_path" in file_info and file_info["rel_path"].endswith((".htm", ".html")):
            # Print link mapper diagnostics for the first few files
            rel_path = file_info["rel_path"]
            print(f"\nDebug info for file: {rel_path}")
            
            # Display how this file is registered in the link map
            norm_path = self.link_mapper._normalize_path(rel_path)
            base_path = os.path.splitext(norm_path)[0]
            
            print(f"Normalized path: {norm_path}")
            print(f"Base path: {base_path}")
            
            # Check various ways this file might be referenced
            variations = [
                norm_path,
                norm_path.lower(),
                base_path,
                base_path.lower(),
            ]
            
            for var in variations:
                if var in self.link_mapper.link_map:
                    print(f"  Found in link map as: {var} → {self.link_mapper.link_map[var]}")
    
    def _copy_assets(self, assets: List[Dict[str, Any]]) -> None:
        """
        Copy assets to the output directory.
        
        Args:
            assets: List of asset dictionaries.
        """
        for asset in assets:
            # Asset paths returned by the parser are absolute. Using them
            # directly avoids accidentally prefixing the input directory twice.
            source_path = Path(asset.get("path", ""))

            if self.preserve_structure:
                rel_path = Path(asset.get("rel_path", asset.get("path", "")))
                # Drop any leading 'Resources' directory from the asset path
                rel_parts = [p for p in rel_path.parts if p.lower() != "resources"]
                rel_path = Path(*rel_parts)
                dest_path = self.output_dir / rel_path
            else:
                # Use new path if provided by LLM
                new_path = Path(asset.get("new_path", asset.get("rel_path", "")))
                rel_parts = [p for p in new_path.parts if p.lower() != "resources"]
                dest_path = self.output_dir / Path(*rel_parts)
            
            # Create parent directories
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Copy the file
            if source_path.exists():
                shutil.copy2(source_path, dest_path)

    def _register_image(self, img_path: str, file_info: Dict[str, Any], output_path: Path) -> Optional[str]:
        """Record an image reference and return the new relative path."""
        html_dir = Path(file_info.get("path", "")).parent

        if os.path.isabs(img_path):
            abs_path = (self.input_dir / img_path.lstrip("/"))
        else:
            abs_path = (html_dir / img_path).resolve()

        if not abs_path.exists():
            return None

        try:
            rel_src = abs_path.relative_to(self.input_dir)
        except ValueError:
            return None

        rel_parts = [p for p in rel_src.parts if p.lower() != "resources"]
        dest_path = self.static_img_dir / Path(*rel_parts)

        self.image_map[abs_path] = dest_path

        new_ref = os.path.relpath(dest_path, output_path.parent).replace("\\", "/")
        return new_ref

    def _copy_tracked_images(self) -> None:
        """Copy all tracked images to the static directory."""
        for src, dest in self.image_map.items():
            if not src.exists():
                continue
            os.makedirs(dest.parent, exist_ok=True)
            if not dest.exists():
                shutil.copy2(src, dest)
    
    def _generate_sidebar(self, structure: Dict[str, Any]) -> None:
        """
        Generate sidebar.js file for Docusaurus.
        
        Args:
            structure: Project structure dictionary.
        """
        sidebar = self.formatter.generate_sidebar_config(structure)
        
        with open(self.output_dir / "sidebars.js", "w", encoding="utf-8") as f:
            f.write("module.exports = ")
            f.write(str(sidebar).replace("'", '"'))
            f.write(";")

    def clean_missing_images(self, verbose: bool = False) -> Dict[str, int]:
        """Scan markdown output for image references that do not exist."""
        static_dir = self.output_dir.parent / "static"
        cleaner = MarkdownImageCleaner(str(self.output_dir), str(static_dir), debug=self.debug)
        return cleaner.clean()
