"""
LLM service for suggesting improved folder/file structure.
"""

import json
from typing import Dict, List, Any, Optional, Union
import requests
import re


class LlmService:
    """
    Service for using LLMs to suggest improvements to document structure.
    """
    
    def __init__(self, api_key: str, provider: str = "openai"):
        """
        Initialize the LLM service.
        
        Args:
            api_key: API key for the LLM provider
            provider: LLM provider ("openai" or "anthropic")
        """
        self.api_key = api_key
        self.provider = provider
        
        # Set up API URLs based on provider
        if provider == "openai":
            self.api_url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            self.model = "gpt-4"
        else:  # anthropic
            self.api_url = "https://api.anthropic.com/v1/messages"
            self.headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
            self.model = "claude-3-sonnet-20240229"
    
    def suggest_structure(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use LLM to suggest improved folder/file structure.
        
        Args:
            project_structure: Dictionary containing the current project structure
            
        Returns:
            Updated project structure with suggested reorganization
        """
        # Extract key information from project structure
        topics = project_structure.get("topics", [])
        toc = project_structure.get("toc", [])
        
        # Create a simplified representation of the structure
        simplified_structure = {
            "project_name": project_structure.get("project_name", ""),
            "topics": [
                {
                    "title": topic.get("title", ""),
                    "path": topic.get("rel_path", ""),
                    "position": topic.get("position", 0),
                } for topic in topics[:50]  # Limit to avoid token limits
            ],
            "toc": [
                {
                    "title": item.get("title", ""),
                    "file": item.get("file", ""),
                    "position": item.get("position", 0),
                } for item in toc[:50]  # Limit to avoid token limits
            ]
        }
        
        # Create the prompt for the LLM
        prompt = self._create_structure_prompt(simplified_structure)
        
        # Call the LLM API
        response = self._call_llm_api(prompt)
        
        # Parse the response
        suggested_structure = self._parse_llm_response(response, project_structure)
        
        return suggested_structure
    
    def _create_structure_prompt(self, structure: Dict[str, Any]) -> str:
        """
        Create a prompt for the LLM to suggest improved structure.
        
        Args:
            structure: Simplified project structure
            
        Returns:
            Prompt string
        """
        prompt = f"""
You are an expert documentation architect specializing in Docusaurus site structure. 
I'm converting a MadCap Flare project to Docusaurus Markdown and need your help to organize the content.

Here's the current structure of the documentation:

Project Name: {structure.get('project_name')}

Topics:
{json.dumps([t for t in structure.get('topics', [])], indent=2)}

Table of Contents:
{json.dumps([t for t in structure.get('toc', [])], indent=2)}

Please analyze this structure and suggest an improved organization for Docusaurus. 
For each file, provide:
1. A new relative path (with .md extension)
2. A sidebar position number
3. Suggested parent topic (if applicable)

Return your answer as a JSON object with the following structure:
{{
  "topics": [
    {{
      "original_path": "path/to/original.html",
      "new_path": "path/to/new.md",
      "sidebar_position": 1,
      "parent": "path/to/parent.md" (optional)
    }},
    ...
  ]
}}

The structure should follow Docusaurus best practices:
- Organize by logical categories
- Keep related content together
- Use clear, descriptive paths
- Have a sensible hierarchy
- Respect existing TOC ordering where appropriate

Only include the original topics in your response, with new suggested paths.
"""
        return prompt
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call the LLM API with the given prompt.
        
        Args:
            prompt: Prompt string
            
        Returns:
            LLM response text
        """
        try:
            if self.provider == "openai":
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
                response = requests.post(self.api_url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            else:  # anthropic
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
                response = requests.post(self.api_url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            # Return a simple response that won't change the structure
            return '{"topics": []}'
    
    def _parse_llm_response(
        self, response: str, original_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse the LLM response and update the project structure.
        
        Args:
            response: LLM response text
            original_structure: Original project structure
            
        Returns:
            Updated project structure
        """
        # Make a copy of the original structure
        updated_structure = original_structure.copy()
        
        try:
            # Extract JSON from the response text
            # First try to find JSON within triple backticks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                # Try to find the JSON object directly
                json_match = re.search(r'(\{.*\})', response, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)
                else:
                    print("Could not extract JSON from LLM response.")
                    return original_structure
            
            # Parse the JSON
            llm_suggestions = json.loads(json_text)
            
            # Create a mapping from original paths to new paths
            path_mapping = {}
            for topic in llm_suggestions.get("topics", []):
                original_path = topic.get("original_path")
                new_path = topic.get("new_path")
                if original_path and new_path:
                    path_mapping[original_path] = topic
            
            # Update the topics with new paths
            for topic in updated_structure.get("topics", []):
                rel_path = topic.get("rel_path", "")
                if rel_path in path_mapping:
                    suggestion = path_mapping[rel_path]
                    topic["new_path"] = suggestion.get("new_path", "")
                    if "sidebar_position" in suggestion:
                        topic["position"] = suggestion["sidebar_position"]
                    if "parent" in suggestion:
                        topic["parent"] = suggestion["parent"]
            
            # Do the same for assets, maintaining the same directory structure as their related topics
            for asset in updated_structure.get("assets", []):
                rel_path = asset.get("rel_path", "")
                # Try to find a matching parent directory in the path mapping
                for orig_path, suggestion in path_mapping.items():
                    if orig_path in rel_path:
                        orig_dir = "/".join(orig_path.split("/")[:-1])
                        new_dir = "/".join(suggestion.get("new_path", "").split("/")[:-1])
                        if orig_dir and new_dir:
                            asset["new_path"] = rel_path.replace(orig_dir, new_dir)
                            break
        
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            # Return the original structure if parsing fails
            return original_structure
        
        return updated_structure 