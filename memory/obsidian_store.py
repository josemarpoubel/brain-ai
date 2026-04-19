"""
Obsidian Store

Semantic memory storage using Markdown-based knowledge graphs.
"""

from typing import Dict, Any, Optional, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ObsidianStore:
    """
    Semantic memory store using Obsidian-compatible Markdown files.
    
    Features:
    - Human-readable contextual knowledge
    - Long-term semantic storage
    - Knowledge graph structure
    """
    
    def __init__(self, base_path: str = "memory/obsidian"):
        """
        Initialize the Obsidian Store.
        
        Args:
            base_path: Base directory for Obsidian vault
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"ObsidianStore initialized at {self.base_path}")
    
    def write_note(self, title: str, content: str, tags: List[str] = None) -> bool:
        """
        Write a note to the Obsidian vault.
        
        Args:
            title: Note title
            content: Note content in Markdown
            tags: List of tags for the note
            
        Returns:
            True if write was successful
        """
        try:
            # Create filename from title
            filename = f"{title.replace(' ', '_')}.md"
            filepath = self.base_path / filename
            
            # Add frontmatter with tags
            markdown_content = self._create_markdown_with_frontmatter(title, content, tags)
            
            filepath.write_text(markdown_content, encoding='utf-8')
            logger.info(f"Note written: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error writing note: {e}")
            return False
    
    def read_note(self, title: str) -> Optional[str]:
        """
        Read a note from the Obsidian vault.
        
        Args:
            title: Note title
            
        Returns:
            Note content or None if not found
        """
        filename = f"{title.replace(' ', '_')}.md"
        filepath = self.base_path / filename
        
        if filepath.exists():
            content = filepath.read_text(encoding='utf-8')
            logger.info(f"Note read: {filename}")
            return content
        
        logger.warning(f"Note not found: {filename}")
        return None
    
    def search_notes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search notes by content or tags.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching notes with metadata
        """
        results = []
        
        # Placeholder implementation
        # In production, would implement full-text search
        logger.info(f"Searching notes for: {query[:50]}...")
        
        return results
    
    def delete_note(self, title: str) -> bool:
        """
        Delete a note from the vault.
        
        Args:
            title: Note title
            
        Returns:
            True if deletion was successful
        """
        filename = f"{title.replace(' ', '_')}.md"
        filepath = self.base_path / filename
        
        if filepath.exists():
            filepath.unlink()
            logger.info(f"Note deleted: {filename}")
            return True
        
        logger.warning(f"Note not found for deletion: {filename}")
        return False
    
    def _create_markdown_with_frontmatter(self, title: str, content: str, tags: List[str] = None) -> str:
        """
        Create Markdown content with YAML frontmatter.
        
        Args:
            title: Note title
            content: Note body content
            tags: List of tags
            
        Returns:
            Complete Markdown string with frontmatter
        """
        markdown = "---\n"
        markdown += f"title: {title}\n"
        
        if tags:
            markdown += f"tags: [{', '.join(tags)}]\n"
        
        markdown += "---\n\n"
        markdown += content
        
        return markdown
    
    def get_all_notes(self) -> List[str]:
        """
        Get list of all note titles.
        
        Returns:
            List of note titles
        """
        notes = []
        for filepath in self.base_path.glob("*.md"):
            notes.append(filepath.stem.replace('_', ' '))
        return notes
