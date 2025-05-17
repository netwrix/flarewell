"""
Image relocation utility for moving images to a specified directory and updating references.
"""

import os
import re
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Set, Pattern, Optional, Tuple, Any


class ImageRelocator:
    """
    Handles relocation of image files to a specified directory and updates references.
    
    This utility handles:
    - Finding image files in the output directory
    - Copying them to a target directory while preserving subdirectory structure 
    - Updating all image references in Markdown files
    """
    
    def __init__(self, 
                 source_dir: str, 
                 target_dir: str, 
                 debug: bool = False,
                 preserve_structure: bool = True):
        """
        Initialize the image relocator.
        
        Args:
            source_dir: Directory containing converted markdown and image files
            target_dir: Target directory for relocated images
            debug: Enable debug logging
            preserve_structure: Whether to maintain subdirectory structure within target directory
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.debug = debug
        self.preserve_structure = preserve_structure
        self.processed_files: Set[str] = set()
        self.relocated_images: Dict[str, str] = {}  # Maps original path to new path
        
        # Configure logging
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("ImageRelocator")
    
    def relocate(self) -> Dict[str, int]:
        """
        Relocate all image files and update references.
        
        Returns:
            Dictionary with relocation statistics
        """
        # Initialize counters
        stats = {
            "images_relocated": 0,
            "files_updated": 0,
            "errors": 0,
        }
        
        # Find all image files
        image_files = self._find_image_files()
        total_images = len(image_files)
        self.logger.info(f"Found {total_images} image files")
        
        # Create target directory if it doesn't exist
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Copy images to target directory
        for source_path in image_files:
            try:
                # Get the path relative to the source directory
                rel_path = source_path.relative_to(self.source_dir)

                # Remove any 'Resources' directory from the relative path
                rel_parts = [p for p in rel_path.parts if p.lower() != "resources"]
                sanitized_parts = [part.replace(" ", "_") for part in rel_parts]
                rel_path_no_res = Path(*sanitized_parts)

                if self.preserve_structure:
                    # Keep subdirectory structure without the Resources folder
                    target_path = self.target_dir / rel_path_no_res
                else:
                    # Flatten structure, just keep filename
                    target_path = self.target_dir / source_path.name.replace(" ", "_")
                
                # Create parent directories if they don't exist
                os.makedirs(target_path.parent, exist_ok=True)
                
                # Move the file so that no copy remains in the docs output
                shutil.copy2(source_path, target_path)
                os.remove(source_path)
                
                # Store the mapping for updating references
                # Include both the original path and the path without 'Resources'
                key_original = str(rel_path).replace("\\", "/")
                key_no_res = str(rel_path_no_res).replace("\\", "/")

                # For the value, calculate the relative path from source_dir to target_path
                # This ensures consistent path resolution regardless of absolute paths
                target_rel_path = os.path.relpath(target_path, self.source_dir)
                for k in {key_original, key_no_res, key_original.lower(), key_no_res.lower()}:
                    self.relocated_images[k] = target_rel_path
                
                stats["images_relocated"] += 1
                
                if self.debug:
                    self.logger.debug(f"Relocated: {rel_path} → {target_rel_path}")
                
            except Exception as e:
                self.logger.error(f"Error relocating {source_path}: {str(e)}")
                stats["errors"] += 1
        
        # Update references in Markdown files
        self.logger.info("Updating image references in Markdown files...")
        markdown_files = list(self.source_dir.glob("**/*.md"))
        
        for md_file in markdown_files:
            try:
                # Read the file content
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Update image references
                updated_content = self._update_image_references(content, md_file)
                
                # Only write back if changes were made
                if updated_content != content:
                    with open(md_file, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    stats["files_updated"] += 1
                    
                    if self.debug:
                        self.logger.debug(f"Updated references in: {md_file.relative_to(self.source_dir)}")
            
            except Exception as e:
                self.logger.error(f"Error updating references in {md_file}: {str(e)}")
                stats["errors"] += 1
        
        return stats
    
    def _find_image_files(self) -> List[Path]:
        """
        Find all image files in the source directory.
        
        Returns:
            List of paths to image files
        """
        # Common image extensions
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"]
        
        # Collect all image files
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(self.source_dir.glob(f"**/*{ext}")))
        
        return image_files
    
    def _update_image_references(self, content: str, current_file: Path) -> str:
        """
        Update image references in Markdown content.
        
        Args:
            content: Markdown content with image references
            current_file: Path of the current file being processed
            
        Returns:
            Updated content with corrected image references
        """
        # Pattern for Markdown image links allowing nested parentheses
        # Format: ![alt text](image/path.jpg "optional title")
        md_image_pattern = (
            r'!\[([^\]]*)\]\('
            r'((?:[^()]|\([^)]*\))*?\.(?:png|jpg|jpeg|gif|svg|bmp|tiff|webp))'
            r'(?:\s+"([^"]*)")?\)'
        )
        
        # Get relative path for the current file
        rel_current_dir = os.path.dirname(str(current_file.relative_to(self.source_dir)))
        
        # Process Markdown image links
        def transform_image_link(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            title_text = match.group(3) or ""
            title = f' "{title_text}"' if title_text else ""
            
            # Skip external images
            if img_path.startswith(('http://', 'https://')):
                return match.group(0)
            
            # Resolve the path
            new_img_path = self._resolve_image_path(img_path, rel_current_dir)
            
            if self.debug:
                self.logger.debug(f"Image: '{img_path}' → '{new_img_path}'")
                
            return f"![{alt_text}]({new_img_path}{title})"
        
        return re.sub(md_image_pattern, transform_image_link, content)
    
    def _resolve_image_path(self, img_path: str, current_dir: str) -> str:
        """Resolve an image path to its new location."""

        # Normalize slashes and remove leading/trailing slashes
        img_path = img_path.replace('\\', '/').strip('/')

        # Determine the absolute path of the referenced image relative to source_dir
        if img_path.startswith('/'):
            abs_path = img_path.lstrip('/')
        else:
            abs_path = os.path.normpath(os.path.join(current_dir, img_path)).replace('\\', '/')

        # Look up relocated path using several fallbacks
        candidates = [abs_path, abs_path.lower()]
        if 'Resources/' in abs_path:
            no_res = abs_path.replace('Resources/', '', 1)
            candidates.extend([no_res, no_res.lower()])

        new_path = None
        for c in candidates:
            if c in self.relocated_images:
                new_path = self.relocated_images[c]
                break

        if new_path:
            try:
                abs_new = os.path.normpath(os.path.join(self.source_dir, new_path))
                abs_current = os.path.normpath(os.path.join(self.source_dir, current_dir))
                rel_path = os.path.relpath(abs_new, abs_current).replace('\\', '/')

                if rel_path.startswith('./') and '/' not in rel_path[2:]:
                    rel_path = rel_path[2:]

                return rel_path
            except ValueError:
                return '/' + new_path

        return img_path
