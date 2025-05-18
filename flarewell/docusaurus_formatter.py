"""
Formatter for converting HTML content to Markdown.

This formatter can output either generic GitHub-Flavoured Markdown or
Docusaurus-flavoured Markdown.  When ``general_markdown`` is ``True`` the
output will avoid Docusaurus specific features such as YAML front matter or
``:::note`` admonitions.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional

WINDOWS_ESCAPE_RE = re.compile(r"\\(?=[ \"'.,;:])")
from html import unescape
from flarewell.link_mapper import LinkMapper

WINDOWS_ESCAPE_RE = re.compile(r"\\(?=[ \t\-_()&'\"])")


def _remove_windows_escapes(text: str) -> str:
    """Remove stray backslash escaping and Windows carriage returns."""
    text = text.replace("\r", "")
    return WINDOWS_ESCAPE_RE.sub("", text)


class DocusaurusFormatter:
    """
    Format HTML content as Docusaurus-compatible Markdown.
    """
    
    def __init__(self, link_mapper: Optional[LinkMapper] = None, general_markdown: bool = False):
        """Initialize the formatter.

        Args:
            link_mapper: Optional ``LinkMapper`` instance for transforming links.
            general_markdown: When ``True`` output generic Markdown rather than
                Docusaurus flavoured Markdown.
        """
        self.link_mapper = link_mapper
        self.general_markdown = general_markdown

    def _remove_windows_escapes(self, text: str) -> str:
        """Remove stray Windows-style escape characters."""
        return WINDOWS_ESCAPE_RE.sub("", text).replace("\r", "")

    def _escape_mdx_braces(self, text: str) -> str:
        """Escape curly braces outside of fenced or inline code blocks."""

        def _escape_segment(segment: str) -> str:
            """Escape braces in a plain text segment without using lookbehind."""
            result = []
            i = 0
            while i < len(segment):
                ch = segment[i]
                # Preserve existing escapes
                if ch == "\\" and i + 1 < len(segment):
                    result.append(ch + segment[i + 1])
                    i += 2
                    continue
                if ch == "{" or ch == "}":
                    result.append("\\" + ch)
                else:
                    result.append(ch)
                i += 1
            return "".join(result)

        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        for i, part in enumerate(parts):
            if part.startswith("```"):
                continue

            subparts = re.split(r'(`[^`]*`)', part)
            for j, sub in enumerate(subparts):
                if sub.startswith('`') and sub.endswith('`'):
                    continue
                subparts[j] = _escape_segment(sub)

            parts[i] = ''.join(subparts)
        return ''.join(parts)

    def _escape_angle_brackets(self, text: str) -> str:
        """Escape `<` and `>` outside of code blocks."""

        def _escape_segment(segment: str) -> str:
            result = []
            i = 0
            while i < len(segment):
                ch = segment[i]
                # Preserve existing escapes
                if ch == "\\" and i + 1 < len(segment):
                    result.append(ch + segment[i + 1])
                    i += 2
                    continue
                if ch == "<" or ch == ">":
                    result.append("\\" + ch)
                else:
                    result.append(ch)
                i += 1
            return "".join(result)

        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        for i, part in enumerate(parts):
            if part.startswith("```"):
                continue

            subparts = re.split(r'(`[^`]*`)', part)
            for j, sub in enumerate(subparts):
                if sub.startswith('`') and sub.endswith('`'):
                    continue
                subparts[j] = _escape_segment(sub)

            parts[i] = ''.join(subparts)

        return ''.join(parts)

    def _sanitize_bad_urls(self, text: str) -> str:
        """Wrap malformed URLs in backticks so MDX does not parse them."""

        def repl(match: re.Match) -> str:
            url = match.group(0)
            # If URL contains a port that is not purely numeric or any
            # obviously invalid characters, wrap it in backticks.
            parsed = re.match(r"https?://[^\s/:]+:(\d+)(/.*)?$", url)
            if (";" in url) or ("(" in url) or (")" in url) or not parsed:
                return f"`{url}`"
            return url

        url_pattern = re.compile(r"https?://[^\s)>]+")
        return url_pattern.sub(repl, text)
    
    def to_markdown(self, content_dict: Dict[str, Any]) -> str:
        """Simplified HTML to Markdown conversion without external deps."""
        html = content_dict.get("content", "")

        # Convert headings
        for i in range(6, 0, -1):
            pattern = re.compile(fr"<h{i}[^>]*>(.*?)</h{i}>", re.IGNORECASE | re.DOTALL)
            html = pattern.sub(lambda m: "\n" + "#" * i + " " + unescape(m.group(1)) + "\n", html)

        # Replace paragraphs and breaks with newlines
        html = re.sub(r"<p[^>]*>", "", html, flags=re.IGNORECASE)
        html = re.sub(r"</p>", "\n\n", html, flags=re.IGNORECASE)
        html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)

        # Drop all other tags
        html = re.sub(r"<[^>]+>", "", html)

        markdown = unescape(html)

        current_file_path = content_dict.get("rel_path", "")
        markdown = self._post_process_markdown(markdown, current_file_path)

        return markdown
    
    
    def _post_process_markdown(self, markdown: str, current_file_path: str = "") -> str:
        """
        Post-process markdown content to apply Docusaurus conventions and ensure all HTML is removed.
        
        Args:
            markdown: Markdown content
            current_file_path: Path of the current file being processed
            
        Returns:
            Processed markdown
        """
        markdown = self._remove_windows_escapes(markdown)

        if not self.general_markdown:
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

        # Wrap malformed URLs so MDX does not attempt to parse them
        markdown = self._sanitize_bad_urls(markdown)

        # Escape curly braces outside of code blocks to avoid MDX parse errors
        markdown = self._escape_mdx_braces(markdown)

        # Escape stray angle brackets which may be interpreted as JSX
        markdown = self._escape_angle_brackets(markdown)
        
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

        # Clean up any stray Windows escaping
        markdown = _remove_windows_escapes(markdown)

        return markdown
    
    def add_frontmatter(
        self, 
        markdown: str, 
        title: str = "", 
        sidebar_position: int = 1,
        description: str = "",
        tags: List[str] = None,
    ) -> str:
        """Add front matter when generating Docusaurus flavoured Markdown."""
        if self.general_markdown:
            return markdown

        title = self._remove_windows_escapes(title).replace('"', '\\"').strip()
        if not title:
            first_line = markdown.split('\n', 1)[0]
            heading = re.match(r"#\s*(.*)", first_line)
            title = heading.group(1).strip() if heading else "Untitled"

        lines = [f'title: "{title}"', f'sidebar_position: {sidebar_position}']

        if description:
            desc = self._remove_windows_escapes(description).replace('"', '\\"')
            lines.append(f'description: "{desc}"')

        if tags:
            lines.append("tags:")
            for tag in tags:
                clean_tag = self._remove_windows_escapes(tag).replace('"', '\\"')
                lines.append(f'  - "{clean_tag}"')

        yaml_content = "\n".join(lines)
        return f"---\n{yaml_content}\n---\n\n{markdown}"
    
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