"""
Parser for MadCap Flare project files and HTML output.
"""

import os
import re
import xml.etree.ElementTree as ET
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


class FlareProjectParser(FlareParserBase):
    """Parser for MadCap Flare project files."""
    
    def __init__(self, input_dir: Union[str, Path], target: Optional[str] = None):
        super().__init__(input_dir)
        self.project_file = None
        self.target = target
        self._find_project_file()
    
    def _find_project_file(self) -> None:
        """Find the .flprj file in the input directory."""
        for file in self.input_dir.glob("*.flprj"):
            self.project_file = file
            break
        
        if not self.project_file:
            raise FileNotFoundError("No .flprj file found in the input directory.")
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse the Flare project and return a structured representation.
        
        Returns:
            Dict containing project structure with topics and assets.
        """
        result = {
            "project_name": self.project_file.stem,
            "topics": [],
            "assets": [],
            "toc": self._parse_toc(),
            "variables": self._parse_variables(),
            "snippets": self._parse_snippets(),
        }
        
        # Find all topics (.htm, .html files)
        content_dir = self.input_dir / "Content"
        if content_dir.exists():
            for file_path in content_dir.glob("**/*.htm*"):
                rel_path = file_path.relative_to(self.input_dir)
                
                topic_info = {
                    "path": str(file_path),
                    "rel_path": str(rel_path),
                    "title": self._extract_title(file_path),
                    "position": len(result["topics"]) + 1,  # Default position
                }
                
                # Try to get position from TOC if available
                for toc_item in result["toc"]:
                    if toc_item.get("file") == str(rel_path):
                        topic_info["position"] = toc_item.get("position", topic_info["position"])
                        topic_info["parent"] = toc_item.get("parent")
                        break
                
                result["topics"].append(topic_info)
        
        # Find all assets (images, etc.)
        resource_dir = self.input_dir / "Resources"
        if resource_dir.exists():
            for file_path in resource_dir.glob("**/*.*"):
                if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf']:
                    rel_path = file_path.relative_to(self.input_dir)
                    result["assets"].append({
                        "path": str(file_path),
                        "rel_path": str(rel_path),
                        "type": file_path.suffix.lower()[1:],
                    })
        
        return result
    
    def _parse_toc(self) -> List[Dict[str, Any]]:
        """Parse the Table of Contents from .fltoc files."""
        result = []
        
        # Find all .fltoc files
        for toc_file in self.input_dir.glob("Project/*.fltoc"):
            try:
                tree = ET.parse(toc_file)
                root = tree.getroot()
                
                # Process TOC entries
                position = 1
                for entry in root.findall(".//TocEntry"):
                    title = entry.get("Title", "")
                    link = entry.get("Link", "")
                    
                    if link:
                        # Extract the path from the link
                        file_path = link.replace("../", "")
                        
                        result.append({
                            "title": title,
                            "file": file_path,
                            "position": position,
                            "parent": None,  # We'll need to add parent-child relationships
                        })
                        
                        position += 1
            except Exception as e:
                print(f"Error parsing TOC file {toc_file}: {str(e)}")
        
        return result
    
    def _parse_variables(self) -> Dict[str, str]:
        """Parse variables from .flvar files."""
        variables = {}
        
        # Find all .flvar files
        for var_file in self.input_dir.glob("Project/VariableSets/*.flvar"):
            try:
                tree = ET.parse(var_file)
                root = tree.getroot()
                
                for variable in root.findall(".//Variable"):
                    name = variable.get("Name", "")
                    value = variable.get("Definition", "")
                    if name and value:
                        variables[name] = value
            except Exception as e:
                print(f"Error parsing variable file {var_file}: {str(e)}")
        
        return variables
    
    def _parse_snippets(self) -> Dict[str, str]:
        """Parse snippets from .flsnp files."""
        snippets = {}
        
        # Find all .flsnp files
        for snippet_file in self.input_dir.glob("Content/**/*.flsnp"):
            try:
                rel_path = snippet_file.relative_to(self.input_dir)
                
                with open(snippet_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                snippets[str(rel_path)] = content
            except Exception as e:
                print(f"Error parsing snippet file {snippet_file}: {str(e)}")
        
        return snippets
    
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
            
            # Extract body content
            body = soup.find("body")
            body_content = str(body) if body else content
            
            # Resolve variables
            body_content = self._resolve_variables(body_content)
            
            # Resolve snippets
            body_content = self._resolve_snippets(body_content)
            
            # Find all images and resources
            images = []
            if body:
                for img in body.find_all("img"):
                    src = img.get("src", "")
                    if src:
                        images.append(src)
            
            return {
                "title": title_text,
                "content": body_content,
                "images": images,
            }
        
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    def _resolve_variables(self, content: str) -> str:
        """Resolve variables in the content."""
        variables = self._parse_variables()
        
        for var_name, var_value in variables.items():
            # Look for variable patterns like {variable.Name}
            pattern = r'\{' + re.escape(var_name) + r'\}'
            content = re.sub(pattern, var_value, content)
        
        return content
    
    def _resolve_snippets(self, content: str) -> str:
        """Resolve snippets in the content."""
        snippets = self._parse_snippets()
        
        # Look for snippet references like <MadCap:snippetText src="SnippetName.flsnp" />
        pattern = r'<MadCap:snippetText\s+src="([^"]+)"\s*/>'
        
        def replace_snippet(match):
            snippet_path = match.group(1)
            # Adjust path if needed (sometimes snippets use relative paths)
            if not snippet_path.startswith("Content/"):
                snippet_path = f"Content/{snippet_path}"
            
            return snippets.get(snippet_path, match.group(0))
        
        return re.sub(pattern, replace_snippet, content)


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
            
            # Find all images and resources
            images = []
            if main_content:
                for img in main_content.find_all("img"):
                    src = img.get("src", "")
                    if src:
                        images.append(src)
            
            return {
                "title": title_text,
                "content": body_content,
                "images": images,
            }
        
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}") 