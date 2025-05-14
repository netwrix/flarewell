"""
Analyzer for MadCap Flare projects to identify production vs test/old content.
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional
import logging


class FlareProjectAnalyzer:
    """
    Analyzes a MadCap Flare project to determine which content is actively used in production.
    """

    def __init__(self, project_dir: str):
        """
        Initialize the analyzer.
        
        Args:
            project_dir: Path to the Flare project directory (containing .flprj file)
        """
        self.project_dir = Path(project_dir)
        self.project_file = None
        self.targets = {}
        self.tocs = {}
        self.logger = logging.getLogger(__name__)
        
        # Find project file
        self._find_project_file()
        
    def _find_project_file(self) -> None:
        """Find the .flprj file in the project directory."""
        for file in self.project_dir.glob("*.flprj"):
            self.project_file = file
            break
        
        if not self.project_file:
            raise FileNotFoundError("No .flprj file found in the project directory.")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the project to determine production vs test/old content.
        
        Returns:
            Dict containing analysis results
        """
        # First load all targets
        self._load_targets()
        
        # Then load all TOCs
        self._load_tocs()
        
        # Determine active outputs
        active_outputs = self._determine_active_outputs()
        
        # Determine used content
        used_topics, unused_topics = self._determine_used_content(active_outputs)
        
        # Determine possible test/old/draft content
        potential_test_content = self._identify_potential_test_content()
        
        # Prepare report
        report = {
            "project_name": self.project_file.stem,
            "active_targets": active_outputs,
            "used_topics": sorted(list(used_topics)),
            "unused_topics": sorted(list(unused_topics)),
            "potential_test_content": potential_test_content,
            "targets": list(self.targets.keys()),
            "tocs": list(self.tocs.keys()),
            "recommendations": self._generate_recommendations(active_outputs, used_topics, potential_test_content)
        }
        
        return report
    
    def _load_targets(self) -> None:
        """Load all target (.fltar) files in the project."""
        # Get target files from project file
        try:
            tree = ET.parse(self.project_file)
            root = tree.getroot()
            
            # Look for target files references in the project
            for url in root.findall(".//Url"):
                source = url.get("Source", "")
                if source.endswith(".fltar"):
                    target_path = self.project_dir / source
                    target_name = Path(source).stem
                    
                    if target_path.exists():
                        try:
                            self.targets[target_name] = {
                                "path": target_path,
                                "tocs": [],
                                "conditions": [],
                                "variables": []
                            }
                            
                            # Parse target file to get TOCs
                            target_tree = ET.parse(target_path)
                            target_root = target_tree.getroot()
                            
                            # Extract TOCs
                            for toc in target_root.findall(".//TocEntry"):
                                toc_path = toc.get("Link", "")
                                if toc_path:
                                    self.targets[target_name]["tocs"].append(toc_path)
                            
                            # TODO: Extract condition tags and variables if needed
                            
                        except Exception as e:
                            self.logger.warning(f"Error parsing target file {target_path}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error loading targets from project file: {str(e)}")
    
    def _load_tocs(self) -> None:
        """Load all TOC (.fltoc) files in the project."""
        # Get TOC files from project file
        try:
            toc_dir = self.project_dir / "Project/TOCs"
            if toc_dir.exists():
                for toc_path in toc_dir.glob("**/*.fltoc"):
                    toc_name = toc_path.stem
                    
                    try:
                        # Parse TOC file
                        toc_tree = ET.parse(toc_path)
                        toc_root = toc_tree.getroot()
                        
                        # Extract topics
                        topics = []
                        for entry in toc_root.findall(".//TocEntry"):
                            link = entry.get("Link", "")
                            title = entry.get("Title", "")
                            
                            if link:
                                # Normalize link path
                                if link.startswith("../"):
                                    link = link[3:]  # Remove ../ prefix
                                
                                topics.append({
                                    "link": link,
                                    "title": title
                                })
                        
                        self.tocs[toc_name] = {
                            "path": toc_path,
                            "topics": topics
                        }
                    
                    except Exception as e:
                        self.logger.warning(f"Error parsing TOC file {toc_path}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error loading TOCs: {str(e)}")
    
    def _determine_active_outputs(self) -> List[str]:
        """
        Determine which targets are likely production outputs.
        
        Returns:
            List of target names that appear to be production targets
        """
        # Check for active target in project file
        active_target = None
        try:
            tree = ET.parse(self.project_file)
            root = tree.getroot()
            active_target = root.get("ActiveTarget")
        except Exception:
            pass
        
        # Start with the active target if specified
        active_outputs = [active_target] if active_target else []
        
        # Look for targets that don't match test/draft patterns
        for target_name in self.targets:
            # Skip targets already in the list
            if target_name in active_outputs:
                continue
            
            # Check for patterns that suggest non-production targets
            test_patterns = [
                r'test', r'draft', r'dev', r'internal', r'qa', r'sandbox', 
                r'example', r'sample', r'old', r'archive', r'deprecated'
            ]
            
            is_test = False
            for pattern in test_patterns:
                if re.search(pattern, target_name, re.IGNORECASE):
                    is_test = True
                    break
            
            if not is_test:
                # This could be a production target
                active_outputs.append(target_name)
        
        return active_outputs
    
    def _determine_used_content(self, active_targets: List[str]) -> Tuple[Set[str], Set[str]]:
        """
        Determine which topics are used in active targets.
        
        Args:
            active_targets: List of active target names
        
        Returns:
            Tuple of (used_topics, unused_topics)
        """
        # Get all topics from all TOCs used by active targets
        used_tocs = set()
        for target_name in active_targets:
            if target_name in self.targets:
                used_tocs.update(self.targets[target_name]["tocs"])
        
        # Get all topics referenced in used TOCs
        used_topics = set()
        for toc_name, toc_data in self.tocs.items():
            # Check if this TOC is used by any active target
            toc_path = str(toc_data["path"].relative_to(self.project_dir))
            if any(toc_path.endswith(used_toc) for used_toc in used_tocs):
                # Add all topics from this TOC
                for topic in toc_data["topics"]:
                    used_topics.add(topic["link"])
        
        # Find all content files in the project
        all_topics = set()
        content_dir = self.project_dir / "Content"
        if content_dir.exists():
            for file_path in content_dir.glob("**/*.htm*"):
                rel_path = str(file_path.relative_to(self.project_dir))
                all_topics.add(rel_path)
        
        # Determine unused topics
        unused_topics = all_topics - used_topics
        
        return used_topics, unused_topics
    
    def _identify_potential_test_content(self) -> Dict[str, List[str]]:
        """
        Identify content that might be test, draft, or deprecated.
        
        Returns:
            Dict with categories of potential test/old content
        """
        # Find content in directories that suggest test/draft content
        test_dirs = []
        draft_dirs = []
        old_dirs = []
        example_dirs = []
        
        content_dir = self.project_dir / "Content"
        if content_dir.exists():
            for directory in content_dir.glob("**/"):
                dir_name = directory.name.lower()
                rel_path = str(directory.relative_to(self.project_dir))
                
                if "test" in dir_name:
                    test_dirs.append(rel_path)
                elif "draft" in dir_name:
                    draft_dirs.append(rel_path)
                elif any(pattern in dir_name for pattern in ["old", "archive", "deprecated"]):
                    old_dirs.append(rel_path)
                elif any(pattern in dir_name for pattern in ["example", "sample"]):
                    example_dirs.append(rel_path)
        
        return {
            "test_directories": test_dirs,
            "draft_directories": draft_dirs,
            "old_directories": old_dirs,
            "example_directories": example_dirs
        }
    
    def _generate_recommendations(
        self, 
        active_targets: List[str], 
        used_topics: Set[str],
        potential_test_content: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Generate recommendations for conversion.
        
        Args:
            active_targets: List of active target names
            used_topics: Set of topics used in active targets
            potential_test_content: Dict with categories of potential test content
            
        Returns:
            Dict with recommendations
        """
        # Generate a set of directories to exclude
        exclude_dirs = []
        exclude_dirs.extend(potential_test_content["test_directories"])
        exclude_dirs.extend(potential_test_content["draft_directories"])
        exclude_dirs.extend(potential_test_content["old_directories"])
        
        # Generate recommendations
        recommendations = {
            "recommended_targets": active_targets[:1] if active_targets else [],  # Default to first active target
            "exclude_directories": exclude_dirs,
            "conversion_options": {
                "preserve_structure": True,
                "convert_unused_topics": False,
            }
        }
        
        return recommendations
    
    def get_target_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of all targets with information.
        
        Returns:
            List of targets with name, path, and description
        """
        targets = []
        
        for target_name, target_data in self.targets.items():
            # Check if target file exists
            target_path = target_data["path"]
            if not target_path.exists():
                continue
            
            # Parse target file to get description
            description = ""
            try:
                tree = ET.parse(target_path)
                root = tree.getroot()
                
                # Look for description (may vary by Flare version)
                desc_elem = root.find(".//Description")
                if desc_elem is not None and desc_elem.text:
                    description = desc_elem.text
            except Exception:
                pass
            
            # Determine if this target is likely a production target
            is_test = False
            test_patterns = [
                r'test', r'draft', r'dev', r'internal', r'qa', r'sandbox', 
                r'example', r'sample', r'old', r'archive', r'deprecated'
            ]
            
            for pattern in test_patterns:
                if re.search(pattern, target_name, re.IGNORECASE):
                    is_test = True
                    break
            
            targets.append({
                "name": target_name,
                "path": str(target_path.relative_to(self.project_dir)),
                "description": description,
                "is_test": is_test,
                "toc_count": len(target_data["tocs"])
            })
        
        # Sort by is_test (production first), then by name
        return sorted(targets, key=lambda x: (x["is_test"], x["name"]))
    
    def get_toc_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of all TOCs with information.
        
        Returns:
            List of TOCs with name, path, and topic count
        """
        tocs = []
        
        for toc_name, toc_data in self.tocs.items():
            tocs.append({
                "name": toc_name,
                "path": str(toc_data["path"].relative_to(self.project_dir)),
                "topic_count": len(toc_data["topics"])
            })
        
        # Sort by topic count (descending), then by name
        return sorted(tocs, key=lambda x: (-x["topic_count"], x["name"]))
    
    def get_folder_stats(self) -> Dict[str, int]:
        """
        Get statistics about folders in the Content directory.
        
        Returns:
            Dict with folder paths and file counts
        """
        folder_stats = {}
        content_dir = self.project_dir / "Content"
        
        if content_dir.exists():
            # First pass: count files in each directory
            for file_path in content_dir.glob("**/*.htm*"):
                parent_dir = str(file_path.parent.relative_to(self.project_dir))
                
                if parent_dir in folder_stats:
                    folder_stats[parent_dir] += 1
                else:
                    folder_stats[parent_dir] = 1
        
        # Sort by file count (descending)
        return dict(sorted(folder_stats.items(), key=lambda x: -x[1]))


def analyze_flare_project(project_dir: str) -> Dict[str, Any]:
    """
    Analyze a MadCap Flare project to determine which content is actively used in production.
    
    Args:
        project_dir: Path to the Flare project directory
        
    Returns:
        Dict containing analysis results
    """
    analyzer = FlareProjectAnalyzer(project_dir)
    return analyzer.analyze()


def list_project_targets(project_dir: str) -> List[Dict[str, Any]]:
    """
    List all targets in a MadCap Flare project.
    
    Args:
        project_dir: Path to the Flare project directory
        
    Returns:
        List of targets with name, path, and description
    """
    analyzer = FlareProjectAnalyzer(project_dir)
    return analyzer.get_target_list()


def list_project_tocs(project_dir: str) -> List[Dict[str, Any]]:
    """
    List all TOCs in a MadCap Flare project.
    
    Args:
        project_dir: Path to the Flare project directory
        
    Returns:
        List of TOCs with name, path, and topic count
    """
    analyzer = FlareProjectAnalyzer(project_dir)
    return analyzer.get_toc_list()


def get_folder_statistics(project_dir: str) -> Dict[str, int]:
    """
    Get statistics about folders in the Content directory.
    
    Args:
        project_dir: Path to the Flare project directory
        
    Returns:
        Dict with folder paths and file counts
    """
    analyzer = FlareProjectAnalyzer(project_dir)
    return analyzer.get_folder_stats() 