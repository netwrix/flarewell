import os
import re
from pathlib import Path
from typing import Dict, Optional, List, Set

class MarkdownImageCleaner:
    """Scan markdown files and remove references to images that do not exist."""

    def __init__(self, docs_dir: str, static_dir: str, debug: bool = False):
        self.docs_dir = Path(docs_dir)
        self.static_dir = Path(static_dir)
        self.debug = debug

    def clean(self) -> Dict[str, int]:
        removed = 0
        removed_files = 0
        all_refs: Set[str] = set()
        details: Dict[str, List[str]] = {}

        md_files = list(self.docs_dir.glob("**/*.md"))
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            updated_content, count, refs = self._remove_missing(content, md_file)
            all_refs.update(refs)
            if count > 0:
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                removed += count
                if self.debug:
                    details[str(md_file.relative_to(self.docs_dir))] = refs

        # Delete unreferenced images from static dir
        image_exts = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"]
        for img_file in self.static_dir.rglob("*"):
            if img_file.suffix.lower() in image_exts and img_file.is_file():
                rel = str(img_file.relative_to(self.docs_dir.parent)).replace("\\", "/")
                if rel not in all_refs and rel.lower() not in {r.lower() for r in all_refs}:
                    if self.debug:
                        print(f"Deleting unreferenced image '{rel}'")
                    img_file.unlink()
                    removed_files += 1

        if self.debug:
            for file, refs in details.items():
                for ref in refs:
                    print(f"Removed '{ref}' from {file}")

        return {"references_removed": removed, "images_deleted": removed_files}

    def _remove_missing(self, text: str, md_file: Path):
        count = 0
        removed: List[str] = []

        def repl_md(match):
            nonlocal count
            img_path = match.group(2)
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
                    return f"![{match.group(1)}]({new_rel})"
                if self.debug:
                    print(f"Removing missing image '{img_path_clean}' in {md_file}")
                count += 1
                removed.append(img_path_clean)
                return ''
            return match.group(0)

        md_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\s*(?:"[^"]*")?\)'
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
                removed.append(img_path_clean)
                return ''
            return match.group(0)

        html_img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
        text = re.sub(html_img_pattern, repl_html, text)

        return text, count, removed

    def _search_nearby_image(self, filename: str) -> Optional[Path]:
        """Search the docs directory for an image with the same filename."""
        matches = list(self.docs_dir.glob(f"**/{filename}"))
        if len(matches) == 1:
            return matches[0]
        return None
