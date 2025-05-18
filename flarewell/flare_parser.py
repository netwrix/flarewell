"""
Parser for MadCap Flare HTML output.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod

import re
from html import unescape


class FlareParserBase(ABC):
    """Base class for Flare parsers."""
    
    def __init__(self, input_dir: Union[str, Path]):
        self.input_dir = Path(input_dir)
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """Parse the input directory and return a structured representation."""
        pass
    
    @abstractmethod
    def get_content(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get the content of a specific file."""
        pass



class FlareHtmlParser(FlareParserBase):
    """Parser for MadCap Flare HTML output."""
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse the HTML output directory.
        
        Returns:
            Dict containing project structure with topics and assets.
        """
        result = {
            "project_name": self.input_dir.name,
            "topics": [],
            "assets": [],
        }
        
        # Find all HTML files
        for file_path in self.input_dir.glob("**/*.htm*"):
            rel_path = file_path.relative_to(self.input_dir)
            
            # Skip files in excluded directories
            excluded_dirs = ["resources", "assets", "scripts", "js", "css", "fonts"]
            if any(part.lower() in excluded_dirs for part in rel_path.parts):
                continue
            
            topic_info = {
                "path": str(file_path),
                "rel_path": str(rel_path),
                "title": self._extract_title(file_path),
                "position": len(result["topics"]) + 1,  # Default position
            }
            
            result["topics"].append(topic_info)
        
        # Find all assets (images, etc.)
        for file_path in self.input_dir.glob("**/*.*"):
            if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf']:
                rel_path = file_path.relative_to(self.input_dir)
                result["assets"].append({
                    "path": str(file_path),
                    "rel_path": str(rel_path),
                    "type": file_path.suffix.lower()[1:],
                })
        
        return result
    
    def _extract_title(self, file_path: Path) -> str:
        """Extract the title from an HTML file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE|re.DOTALL)
            if title_match:
                return unescape(title_match.group(1).strip())

            h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE|re.DOTALL)
            if h1_match:
                return unescape(h1_match.group(1).strip())
            
            # Fallback to filename
            return file_path.stem
        except Exception:
            return file_path.stem
    
    def get_content(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the content of a specific file.
        
        Args:
            file_info: Dictionary with file information.
            
        Returns:
            Dict with content and metadata.
        """
        file_path = file_info.get("path")
        if not file_path:
            raise ValueError("No file path provided in file_info")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE|re.DOTALL)
            title_text = unescape(title_match.group(1).strip()) if title_match else file_info.get("title", "")
            
            body_match = re.search(r"<body[^>]*>(.*)</body>", content, re.IGNORECASE|re.DOTALL)
            body_content = body_match.group(1) if body_match else content

            image_paths = re.findall(r'<img[^>]+src="([^"]+)"', body_content, flags=re.IGNORECASE)
            images = [p.replace('\\', '/') for p in image_paths]
            
            return {
                "title": title_text,
                "content": body_content,
                "images": images,
            }
        
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}") 