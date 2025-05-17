"""
Formatter for converting HTML content to Docusaurus-compatible Markdown.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from flarewell.link_mapper import LinkMapper


class DocusaurusFormatter:
    """
    Format HTML content as Docusaurus-compatible Markdown.
    """
    
    def __init__(self, link_mapper: Optional[LinkMapper] = None):
        """
        Initialize the formatter with optional link mapper.
        
        Args:
            link_mapper: Optional LinkMapper instance for transforming links
        """
        self.link_mapper = link_mapper
    
    def to_markdown(self, content_dict: Dict[str, Any]) -> str:
        """
        Convert HTML content to Markdown.
        
        Args:
            content_dict: Dictionary with content and metadata.
            
        Returns:
            Markdown string.
        """
        content = content_dict.get("content", "")
        
        # Parse with BeautifulSoup to clean up HTML
        soup = BeautifulSoup(content, "html.parser")
        
        # Remove unwanted elements (navigation, scripts, etc.)
        for element in soup.select("script, style, nav, .navigation, .toolbar, .breadcrumbs, .footer"):
            element.decompose()
        
        # Store expandable sections for later processing
        toggle_sections = []
        
        # Extract toggle sections before conversion
        for toggle in soup.select(".toggleButton, .MCToggleButton"):
            section = toggle.find_next("div", class_=["toggleSection", "MCToggleSection"])
            if section:
                toggle_text = toggle.get_text().strip()
                section_content = section.get_text().strip()
                toggle_sections.append({
                    "title": toggle_text,
                    "content": section_content
                })
                
                # Remove these elements so they don't get processed by markdownify
                toggle.decompose()
                section.decompose()
        
        # Convert Flare-specific elements to Docusaurus equivalents
        self._convert_flare_elements(soup)
        
        # Convert to markdown using markdownify with all HTML elements converted
        markdown = md(str(soup), heading_style="ATX", bullets="*", strip=["body", "html"])
        
        # Post-process the markdown
        current_file_path = content_dict.get("rel_path", "")
        markdown = self._post_process_markdown(markdown, current_file_path)
        
        # Add the expandable sections back
        for i, section in enumerate(toggle_sections):
            details_markdown = f"\n<details>\n<summary>{section['title']}</summary>\n\n{section['content']}\n</details>\n\n"
            # Add details after the corresponding section (typically after installation)
            if i == 0 and "## Installation" in markdown:
                install_section_end = markdown.find("##", markdown.find("## Installation") + 12)
                if install_section_end == -1:
                    install_section_end = len(markdown)
                markdown = markdown[:install_section_end] + details_markdown + markdown[install_section_end:]
            else:
                # If we can't find a good place, append to the end
                markdown += details_markdown
        
        return markdown
    
    def _convert_flare_elements(self, soup: BeautifulSoup) -> None:
        """
        Convert Flare-specific HTML elements to equivalent Docusaurus markdown patterns.
        
        Args:
            soup: BeautifulSoup instance of the HTML.
        """
        # Convert notes
        for note in soup.select(".note, .MCNote"):
            note_text = note.get_text().strip()
            note_tag = soup.new_tag("div")
            note_tag.string = f":::note\n{note_text}\n:::"
            note.replace_with(note_tag)
        
        # Convert warnings
        for warning in soup.select(".warning, .MCWarning"):
            warning_text = warning.get_text().strip()
            warning_tag = soup.new_tag("div")
            warning_tag.string = f":::warning\n{warning_text}\n:::"
            warning.replace_with(warning_tag)
        
        # Convert tips
        for tip in soup.select(".tip, .MCTip"):
            tip_text = tip.get_text().strip()
            tip_tag = soup.new_tag("div")
            tip_tag.string = f":::tip\n{tip_text}\n:::"
            tip.replace_with(tip_tag)
        
        # Convert tables - ensure they have headers for proper markdown conversion
        for table in soup.select("table"):
            # Ensure tables have proper structure for Markdown
            if not table.find("thead"):
                # If no header, add an empty one for markdown conversion
                thead = soup.new_tag("thead")
                tr = soup.new_tag("tr")
                
                # Get number of columns
                first_row = table.find("tr")
                if first_row:
                    num_cols = len(first_row.find_all(["td", "th"]))
                    for _ in range(num_cols):
                        th = soup.new_tag("th")
                        th.string = " "  # Empty header
                        tr.append(th)
                    
                    thead.append(tr)
                    
                    # Insert the header at the beginning of the table
                    table.insert(0, thead)
        
        # Convert MadCap-specific elements to markdown equivalents
        for xref in soup.select("MadCap\\:xref"):
            href = xref.get("href", "")
            text = xref.get_text().strip()
            
            # Create a standard link
            link = soup.new_tag("a")
            link["href"] = href
            link.string = text
            
            xref.replace_with(link)
        
        # Preserve image paths with original structure for later relocation
        for img in soup.select("img"):
            src = img.get("src", "")
            if src:
                # Keep the original path but normalize slashes
                normalized_src = src.replace("\\", "/")
                img["src"] = normalized_src
    
    def _post_process_markdown(self, markdown: str, current_file_path: str = "") -> str:
        """
        Post-process markdown content to apply Docusaurus conventions and ensure all HTML is removed.
        
        Args:
            markdown: Markdown content
            current_file_path: Path of the current file being processed
            
        Returns:
            Processed markdown
        """
        # Fix admonitions (notes, warnings, tips)
        markdown = re.sub(r':::note\s+', ":::note\n", markdown)
        markdown = re.sub(r':::warning\s+', ":::warning\n", markdown)
        markdown = re.sub(r':::tip\s+', ":::tip\n", markdown)
        
        # Use link mapper to transform links if available
        if self.link_mapper and current_file_path:
            markdown = self.link_mapper.transform_links(markdown, current_file_path)
        else:
            # Legacy link handling if no link mapper is available
            # Fix internal links by removing extensions
            markdown = re.sub(r'\]\(([^)]+)\.(htm|html)\)', r'](\1)', markdown)
        
        # Preserve original image paths (don't modify them here)
        # This allows the image relocator to handle them correctly later
        # Only normalize any Resource/Images references to avoid duplicate slashes
        markdown = re.sub(r'\]\(Resources/+Images/', r'](Resources/Images/', markdown)
        
        # Remove extra blank lines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Fix code blocks
        markdown = re.sub(r'```\s+', '```\n', markdown)
        
        # Fix any remaining HTML artifacts
        # Convert any remaining <br> tags to newlines
        markdown = re.sub(r'<br\s*/?>', '\n', markdown)
        
        # Fix details/summary to use proper format
        markdown = re.sub(
            r'<details>\s*<summary>(.*?)</summary>\s*(.*?)\s*</details>',
            r'<details>\n<summary>\1</summary>\n\n\2\n</details>',
            markdown,
            flags=re.DOTALL
        )
        
        # Remove any remaining HTML tags except for details/summary
        markdown = re.sub(r'<(?!(details|\/details|summary|\/summary))[^>]*>', '', markdown)
        
        return markdown
    
    def add_frontmatter(
        self, 
        markdown: str, 
        title: str = "", 
        sidebar_position: int = 1,
        description: str = "",
        tags: List[str] = None,
    ) -> str:
        """
        Add Docusaurus front matter to markdown content.
        
        Args:
            markdown: Markdown content
            title: Document title
            sidebar_position: Position in the sidebar
            description: Document description
            tags: List of tags
            
        Returns:
            Markdown with front matter
        """
        front_matter = {
            "title": title,
            "sidebar_position": sidebar_position,
        }
        
        if description:
            front_matter["description"] = description
        
        if tags:
            front_matter["tags"] = tags
        
        # Convert to YAML
        yaml_content = yaml.dump(front_matter, default_flow_style=False)
        
        # Combine front matter and markdown
        result = f"---\n{yaml_content}---\n\n{markdown}"
        
        return result
    
    def generate_sidebar_config(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sidebar configuration for Docusaurus.
        
        Args:
            structure: Project structure dictionary.
            
        Returns:
            Sidebar configuration.
        """
        # Build basic sidebar structure from TOC
        toc_items = structure.get("toc", [])
        topics = structure.get("topics", [])
        
        # Create a mapping of file paths to topic info
        topic_map = {}
        for topic in topics:
            rel_path = topic.get("rel_path", "")
            if rel_path:
                topic_map[rel_path] = topic
        
        # Sort TOC items by position
        toc_items = sorted(toc_items, key=lambda x: x.get("position", 0))
        
        # Build sidebar items
        sidebar_items = []
        for item in toc_items:
            file_path = item.get("file", "")
            if file_path in topic_map:
                # Convert file path to docusaurus path
                # Remove extension and transform to match Docusaurus slugs
                docusaurus_path = file_path.rsplit(".", 1)[0]
                
                sidebar_item = {
                    "type": "doc",
                    "id": docusaurus_path,
                    "label": item.get("title", topic_map[file_path].get("title", "")),
                }
                
                sidebar_items.append(sidebar_item)
        
        # Create the final sidebar config
        sidebar = {
            "sidebar": sidebar_items
        }
        
        return sidebar 