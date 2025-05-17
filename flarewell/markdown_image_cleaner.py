import os
import re
from pathlib import Path
from typing import Dict, Optional

class MarkdownImageCleaner:
    """Scan markdown files and remove references to images that do not exist."""

    def __init__(self, docs_dir: str, debug: bool = False):
        self.docs_dir = Path(docs_dir)
        self.debug = debug

    def clean(self) -> Dict[str, int]:
        removed = 0
        md_files = list(self.docs_dir.glob("**/*.md"))
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            updated_content, count = self._remove_missing(content, md_file)
            if count > 0:
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                removed += count
        return {"references_removed": removed}

    def _remove_missing(self, text: str, md_file: Path):
        count = 0

        def repl_md(match):
            nonlocal count
            img_path = match.group(2)
            img_path_clean = img_path.split()[0].replace('\\', '/').strip()
            if img_path_clean.startswith(('http://', 'https://')):
                return match.group(0)
            abs_path = (md_file.parent / img_path_clean).resolve()
            if not abs_path.exists():
                candidate = self._search_nearby_image(Path(img_path_clean).name)
                if candidate:
                    new_rel = os.path.relpath(candidate, md_file.parent).replace('\\', '/')
                    if self.debug:
                        print(
                            f"Fixed missing image '{img_path_clean}' -> '{new_rel}' in {md_file}"
                        )
                    return f"![{match.group(1)}]({new_rel})"
                if self.debug:
                    print(f"Removing missing image '{img_path_clean}' in {md_file}")
                count += 1
                return ''
            return match.group(0)

        md_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        text = re.sub(md_image_pattern, repl_md, text)

        def repl_html(match):
            nonlocal count
            img_path = match.group(1)
            img_path_clean = img_path.replace('\\', '/').strip()
            if img_path_clean.startswith(('http://', 'https://')):
                return match.group(0)
            abs_path = (md_file.parent / img_path_clean).resolve()
            if not abs_path.exists():
                candidate = self._search_nearby_image(Path(img_path_clean).name)
                if candidate:
                    new_rel = os.path.relpath(candidate, md_file.parent).replace('\\', '/')
                    if self.debug:
                        print(
                            f"Fixed missing image '{img_path_clean}' -> '{new_rel}' in {md_file}"
                        )
                    return match.group(0).replace(img_path, new_rel)
                if self.debug:
                    print(f"Removing missing image '{img_path_clean}' in {md_file}")
                count += 1
                return ''
            return match.group(0)

        html_img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
        text = re.sub(html_img_pattern, repl_html, text)

        return text, count

    def _search_nearby_image(self, filename: str) -> Optional[Path]:
        """Search the docs directory for an image with the same filename."""
        matches = list(self.docs_dir.glob(f"**/{filename}"))
        if len(matches) == 1:
            return matches[0]
        return None
