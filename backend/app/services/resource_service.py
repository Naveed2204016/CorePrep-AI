"""
Helper service to generate and manage topic resources (blogs, videos)
This can be called to auto-suggest resources for topics
"""

from typing import List, Dict, Any
import json
from langchain_core.prompts import ChatPromptTemplate
from app.core.llm_config import get_llm


class ResourceGenerationService:
    """Generate learning resources for topics"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def suggest_resources(
        self, 
        topic: str, 
        subject: str,
        num_blogs: int = 2,
        num_videos: int = 2
    ) -> Dict[str, Any]:
        """
        Suggest blogs and videos for a topic
        Note: These are suggestions. In production, you'd verify links work.
        
        Returns: {
            "blogs": [{"title": str, "url": str, "description": str}, ...],
            "videos": [{"title": str, "url": str, "description": str}, ...]
        }
        """
        
        prompt = ChatPromptTemplate.from_template(
            """Suggest high-quality learning resources for this topic.

Subject: {subject}
Topic: {topic}

Suggest {num_blogs} blog articles and {num_videos} YouTube videos.
These should be:
- From reputable sources (GeeksforGeeks, Medium, etc.)
- Clear and educational
- Covering different aspects/difficulty levels

Return as JSON only (no markdown):
{{
    "blogs": [
        {{
            "title": "Blog title",
            "url": "https://...",
            "description": "What this resource covers"
        }},
        ...
    ],
    "videos": [
        {{
            "title": "Video title",
            "url": "https://www.youtube.com/watch?v=...",
            "description": "What this video teaches"
        }},
        ...
    ]
}}

Note: Suggest real, well-known resources. Use these sources:
- GeeksforGeeks.org
- Medium.com
- YouTube.com (real channels)
- Official documentation"""
        )
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "subject": subject,
                "topic": topic,
                "num_blogs": num_blogs,
                "num_videos": num_videos
            })
            
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content.strip())
        
        except Exception as e:
            # Return default resources if LLM fails
            return self._get_default_resources(topic, subject)
    
    def _get_default_resources(self, topic: str, subject: str):
        """Fallback default resources"""
        return {
            "blogs": [
                {
                    "title": f"{topic} - GeeksforGeeks",
                    "url": f"https://www.geeksforgeeks.org/",
                    "description": f"Comprehensive guide to {topic}"
                }
            ],
            "videos": [
                {
                    "title": f"{topic} Explained",
                    "url": "https://www.youtube.com/results?search_query=" + topic.replace(" ", "+"),
                    "description": f"Video tutorials on {topic}"
                }
            ]
        }


def get_resource_service():
    """Get resource generation service"""
    return ResourceGenerationService()
