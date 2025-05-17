"""
Parser for MadCap Flare HTML output.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


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
            
            soup = BeautifulSoup(content, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                return title_tag.text.strip()
            
            # Look for h1 if no title
            h1_tag = soup.find("h1")
            if h1_tag:
                return h1_tag.text.strip()
            
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
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")
            
            # Extract title
            title = soup.find("title")
            title_text = title.text.strip() if title else file_info.get("title", "")
            
            # Find the main content div (typical in Flare HTML output)
            main_content = soup.find(class_="MCWikiCategory") or \
                          soup.find(class_="MCWikiArticle") or \
                          soup.find(class_="topic") or \
                          soup.find(id="contentBody") or \
                          soup.find("body")
            
            body_content = str(main_content) if main_content else str(soup.body)
            
            # Collect image references for post-processing
            images = []
            if main_content:
                for img in main_content.find_all("img"):
                    src = img.get("src", "")
                    if not src:
                        continue

                    normalized_src = src.replace("\\", "/")
                    images.append(normalized_src)
            
            return {
                "title": title_text,
                "content": body_content,
                "images": images,
            }
        
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}") 