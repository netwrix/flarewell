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

from bs4 import BeautifulSoup
import markdownify

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

    def __init__(
        self, link_mapper: Optional[LinkMapper] = None, general_markdown: bool = False
    ):
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

        parts = re.split(r"(```.*?```)", text, flags=re.DOTALL)
        for i, part in enumerate(parts):
            if part.startswith("```"):
                continue

            parts[i] = _escape_segment(part)
        return "".join(parts)

    def _escape_angle_brackets(self, text: str) -> str:
        """Escape `<` and `>` outside of code blocks by using HTML entities."""

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
                if ch == "<":
                    result.append("&lt;")
                elif ch == ">":
                    result.append("&gt;")
                else:
                    result.append(ch)
                i += 1
            return "".join(result)

        parts = re.split(r"(```.*?```)", text, flags=re.DOTALL)
        for i, part in enumerate(parts):
            if part.startswith("```"):
                continue

            subparts = re.split(r"(`[^`]*`)", part)
            for j, sub in enumerate(subparts):
                if sub.startswith("`") and sub.endswith("`"):
                    continue
                subparts[j] = _escape_segment(sub)

            parts[i] = "".join(subparts)

        return "".join(parts)

    def _sanitize_bad_urls(self, text: str) -> str:
        """Wrap malformed URLs in backticks so MDX does not parse them."""

        # url_pattern captures the URL in group 1 and the character following it in group 2
        # This helps determine if the URL is followed by problematic punctuation.
        url_pattern = re.compile(
            r'''(https?://(?:[a-zA-Z0-9\-_.~!*'();:@&=+$,/?%#\[\]]+\.)+(?:[a-zA-Z]{2,}|[0-9]{1,3})(?::\d+)?(?:/[a-zA-Z0-9\-_.~!*'();:@&=+$,/?%#\[\]]*)?)([^\w\-/.]|\s|$)'''
        )

        def repl(match: re.Match) -> str:
            url = match.group(1)
            trailing_char = match.group(2) # Character immediately following the URL

            # Check for invalid port
            port_match = re.match(r"https?://[^\s/:]+:(\d+)(/.*)?$", url)
            is_port_valid = bool(port_match)

            # Characters that, if trailing the URL, require the URL to be wrapped
            problematic_trailing_chars = [")", "!", "?", ","] # Period is handled by regex

            wrap_url = False
            if not is_port_valid:
                wrap_url = True
            elif any(c in url for c in [";", "(", ")"]): # Unbalanced or problematic chars within URL
                wrap_url = True
            elif trailing_char in problematic_trailing_chars:
                wrap_url = True
            # Special case for period: only wrap if it's not part of the URL itself
            # The regex already ensures period is not part of trailing_char unless it's the *only* trailing char
            elif trailing_char == '.' and not url.endswith('.'): # e.g. URL followed by period then space
                 wrap_url = True


            if wrap_url:
                return f"`{url}`{trailing_char}"
            else:
                # Return the original full match (URL + trailing character)
                return match.group(0)

        return url_pattern.sub(repl, text)

    def _fix_code_blocks(self, text: str) -> str:
        """Ensure code fences have a language and escape problematic characters."""

        code_block_pattern = re.compile(
            r"```(?P<lang>[^\n]*)\n(?P<code>.*?)```", re.DOTALL
        )

        def repl(match: re.Match) -> str:
            lang = match.group("lang").strip()
            code = match.group("code")

            if not lang:
                lang = "text"

            # Escape braces which confuse MDX
            code = code.replace("{", "\\{").replace("}", "\\}")

            # Escape percent signs in shell-style blocks
            if lang.lower() in [
                "bash",
                "cmd",
                "powershell",
                "shell",
                "bat",
                "console",
                "sh",
                "zsh",
            ]:
                code = code.replace("%", "\\%")

            return f"```{lang}\n{code}```"

        return code_block_pattern.sub(repl, text)

    def _escape_inline_code(self, text: str) -> str:
        """Escape braces inside inline code segments."""

        inline_code_pattern = re.compile(r"`([^`]*?(?:\\{|\\})[^`]*)`")

        def repl(match: re.Match) -> str:
            code = match.group(1)
            code = code.replace("{", "\\{").replace("}", "\\}")
            return f"`{code}`"

        return inline_code_pattern.sub(repl, text)

    def _escape_jsx_like(self, text: str) -> str:
        """Wrap HTML-like tags in backticks to avoid MDX JSX parsing."""

        jsx_pattern = re.compile(
            r"(?<!`)(<[a-zA-Z][^<>]*>[^<>]*</[a-zA-Z][^<>]*>|<[a-zA-Z][^<>]*/>)(?!`)"
        )

        return jsx_pattern.sub(lambda m: f"`{m.group(0)}`", text)

    def to_markdown(self, content_dict: Dict[str, Any]) -> str:
        """Convert HTML content to Markdown using ``markdownify`` and BeautifulSoup."""
        html = content_dict.get("content", "")

        # Parse with BeautifulSoup to clean malformed HTML
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Use markdownify for robust HTML -> Markdown conversion
        markdown = markdownify.markdownify(str(soup), heading_style="ATX")

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
            markdown = re.sub(r":::note\s+", ":::note\n", markdown)
            markdown = re.sub(r":::warning\s+", ":::warning\n", markdown)
            markdown = re.sub(r":::tip\s+", ":::tip\n", markdown)

        # Use link mapper to transform links if available
        if self.link_mapper and current_file_path:
            markdown = self.link_mapper.transform_links(markdown, current_file_path)
        else:
            # Legacy link handling if no link mapper is available
            # Fix internal links by removing extensions
            markdown = re.sub(r"\]\(([^)]+)\.(htm|html)\)", r"](\1)", markdown)

        # Preserve original image paths (don't modify them here)
        # This allows the image relocator to handle them correctly later
        # Only normalize any Resource/Images references to avoid duplicate slashes
        markdown = re.sub(r"\]\(Resources/+Images/", r"](Resources/Images/", markdown)

        # Remove extra blank lines
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # Fix code blocks and escape special characters inside them
        markdown = re.sub(r"```\s+", "```\n", markdown)
        markdown = self._fix_code_blocks(markdown)

        # Escape braces inside inline code
        markdown = self._escape_inline_code(markdown)

        # Escape stray angle brackets which may be interpreted as JSX
        # This should run before _escape_mdx_braces and _escape_jsx_like
        markdown = self._escape_angle_brackets(markdown)

        # Escape curly braces outside of code blocks to avoid MDX parse errors
        # Runs after angle brackets are escaped, and after code blocks/inline code have handled their braces.
        markdown = self._escape_mdx_braces(markdown)

        # Wrap HTML-like tags in backticks so MDX doesn't treat them as JSX
        # Runs after angle brackets and braces are escaped. Its original pattern
        # will likely not match anymore if _escape_angle_brackets is effective.
        markdown = self._escape_jsx_like(markdown)

        # Wrap malformed URLs so MDX does not attempt to parse them
        markdown = self._sanitize_bad_urls(markdown)

        # Fix any remaining HTML artifacts
        # Convert any remaining <br> tags to newlines
        markdown = re.sub(r"<br\s*/?>", "\n", markdown)

        # Fix details/summary to use proper format
        markdown = re.sub(
            r"<details>\s*<summary>(.*?)</summary>\s*(.*?)\s*</details>",
            r"<details>\n<summary>\1</summary>\n\n\2\n</details>",
            markdown,
            flags=re.DOTALL,
        )

        # Remove any remaining HTML tags except for details/summary
        markdown = re.sub(
            r"<(?!(details|\/details|summary|\/summary))[^>]*>", "", markdown
        )

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
            first_line = markdown.split("\n", 1)[0]
            heading = re.match(r"#\s*(.*)", first_line)
            title = heading.group(1).strip() if heading else "Untitled"

        lines = [f'title: "{title}"', f"sidebar_position: {sidebar_position}"]

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
        sidebar = {"sidebar": sidebar_items}

        return sidebar
