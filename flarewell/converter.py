"""
Core conversion functionality for Flarewell.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from bs4 import BeautifulSoup
import html2markdown
import yaml

from flarewell.flare_parser import FlareHtmlParser
from flarewell.docusaurus_formatter import DocusaurusFormatter
from flarewell.link_mapper import LinkMapper
from flarewell.llm_service import LlmService


class FlareConverter:
    """Convert Flare content to Markdown."""

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        preserve_structure: bool = True,
        use_llm: bool = False,
        llm_api_key: Optional[str] = None,
        llm_provider: str = "openai",
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
            use_llm: Whether to call an LLM for structure suggestions.
            llm_api_key: API key for the LLM if ``use_llm`` is ``True``.
            llm_provider: LLM provider name.
            target: Optional Flare target to build from.
            exclude_dirs: Directories to exclude from conversion.
            debug: Enable verbose logging.
            markdown_style: ``"docusaurus"`` or ``"markdown"``.
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.preserve_structure = preserve_structure
        self.use_llm = use_llm
        self.llm_api_key = llm_api_key
        self.llm_provider = llm_provider
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
        
        # Initialize LLM service if requested
        self.llm_service = None
        if use_llm and llm_api_key:
            self.llm_service = LlmService(api_key=llm_api_key, provider=llm_provider)

    def convert(self) -> Dict[str, int]:
        """
        Main conversion process.
        
        Returns:
            Dict with conversion statistics.
        """
        # Parse the Flare HTML structure
        project_structure = self.parser.parse()
        
        # Optionally use LLM to reorganize the structure
        if self.use_llm and self.llm_service:
            project_structure = self.llm_service.suggest_structure(project_structure)
        
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
        
        # Copy assets
        self._copy_assets(project_structure.get("assets", []))
        
        # Generate sidebar.js if needed
        if not self.preserve_structure and self.use_llm:
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
        
        # Convert to markdown
        md_content = self.formatter.to_markdown(content)
        
        # Add front matter
        md_content = self.formatter.add_frontmatter(
            md_content, 
            title=file_info.get("title", ""),
            sidebar_position=file_info.get("position", 1),
            description=file_info.get("description", ""),
        )
        
        # Determine output path
        if self.preserve_structure:
            rel_path = file_info.get("rel_path", file_info.get("path", ""))
            output_path = self.output_dir / rel_path
        else:
            # Use new path if provided by LLM
            output_path = self.output_dir / file_info.get("new_path", file_info.get("rel_path", ""))
        
        # Ensure the path has .md extension
        output_path = output_path.with_suffix(".md")
        
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
            source_path = self.input_dir / asset.get("path", "")
            
            if self.preserve_structure:
                rel_path = asset.get("rel_path", asset.get("path", ""))
                dest_path = self.output_dir / rel_path
            else:
                # Use new path if provided by LLM
                dest_path = self.output_dir / asset.get("new_path", asset.get("rel_path", ""))
            
            # Create parent directories
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Copy the file
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
    
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