"""
Blood Ledger — Conversation Thread Handling

Conversation threads are markdown files that store the actual dialogue and narration
for player-experienced history. Narratives point to sections within these files.

File structure:
    conversations/
        char_aldric.md      # All conversations with Aldric
        char_edmund.md      # All conversations with Edmund
        scene_001.md        # Scene-based if preferred

Section format:
    ## Day 4, Night — The Camp

    Aldric stares into the fire. He hasn't spoken in an hour.

    You: "You fought at Stamford Bridge."
    Aldric: "Aye."
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ConversationSection:
    """A section of conversation from a thread file."""
    header: str
    content: str
    file_path: str


class ConversationThread:
    """
    Manages conversation thread files for player-experienced history.

    Each conversation is stored as a markdown file with sections marked by ## headers.
    Narratives reference specific sections via {file, section} pointers.
    """

    def __init__(self, base_dir: str):
        """
        Initialize conversation thread manager.

        Args:
            base_dir: Base directory for conversation files
                      e.g., "playthroughs/abc123/conversations"
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, character_id: str) -> Path:
        """Get the conversation file path for a character."""
        # char_aldric -> aldric.md
        name = character_id.replace("char_", "")
        return self.base_dir / f"{name}.md"

    def _get_relative_path(self, character_id: str) -> str:
        """Get relative path for storage in narrative source."""
        name = character_id.replace("char_", "")
        return f"conversations/{name}.md"

    def append_section(
        self,
        character_id: str,
        day: int,
        time_of_day: str,
        location_name: str,
        content: str
    ) -> Dict[str, str]:
        """
        Append a new conversation section to the character's thread.

        Args:
            character_id: e.g., "char_aldric"
            day: Day number (1-based)
            time_of_day: e.g., "night", "morning"
            location_name: Human-readable location name
            content: The conversation/narration text

        Returns:
            Dict with 'file' and 'section' for narrative source reference
        """
        file_path = self._get_file_path(character_id)
        section_header = f"Day {day}, {time_of_day.capitalize()} — {location_name}"

        # Create file with header if it doesn't exist
        if not file_path.exists():
            char_name = character_id.replace("char_", "").replace("_", " ").title()
            file_path.write_text(f"# Conversations with {char_name}\n\n")

        # Append the new section
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n## {section_header}\n\n")
            f.write(content.strip())
            f.write("\n")

        logger.info(f"[Conversations] Appended section '{section_header}' to {file_path}")

        return {
            "file": self._get_relative_path(character_id),
            "section": section_header
        }

    def read_section(self, file_path: str, section_header: str) -> Optional[str]:
        """
        Read a specific section from a conversation file.

        Args:
            file_path: Relative path like "conversations/aldric.md"
            section_header: Section header like "Day 4, Night — The Camp"

        Returns:
            Section content, or None if not found
        """
        full_path = self.base_dir.parent / file_path

        if not full_path.exists():
            logger.warning(f"[Conversations] File not found: {full_path}")
            return None

        content = full_path.read_text(encoding="utf-8")

        # Find the section
        # Pattern: ## {header}\n\n{content until next ## or EOF}
        pattern = rf"## {re.escape(section_header)}\n\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            return match.group(1).strip()
        else:
            logger.warning(f"[Conversations] Section not found: '{section_header}' in {file_path}")
            return None

    def list_sections(self, character_id: str) -> List[str]:
        """
        List all section headers in a character's conversation file.

        Args:
            character_id: e.g., "char_aldric"

        Returns:
            List of section header strings
        """
        file_path = self._get_file_path(character_id)

        if not file_path.exists():
            return []

        content = file_path.read_text(encoding="utf-8")
        headers = re.findall(r"^## (.+)$", content, re.MULTILINE)
        return headers

    def get_full_thread(self, character_id: str) -> Optional[str]:
        """
        Get the complete conversation thread for a character.

        Args:
            character_id: e.g., "char_aldric"

        Returns:
            Full file content, or None if file doesn't exist
        """
        file_path = self._get_file_path(character_id)

        if not file_path.exists():
            return None

        return file_path.read_text(encoding="utf-8")

    def search_sections(
        self,
        character_id: str,
        keyword: str
    ) -> List[ConversationSection]:
        """
        Search for sections containing a keyword.

        Args:
            character_id: e.g., "char_aldric"
            keyword: Text to search for

        Returns:
            List of matching ConversationSections
        """
        file_path = self._get_file_path(character_id)

        if not file_path.exists():
            return []

        content = file_path.read_text(encoding="utf-8")
        results = []

        # Split into sections
        sections = re.split(r"\n## ", content)
        for section in sections[1:]:  # Skip the title section
            if keyword.lower() in section.lower():
                # Extract header (first line)
                lines = section.split("\n", 1)
                header = lines[0].strip()
                section_content = lines[1].strip() if len(lines) > 1 else ""

                results.append(ConversationSection(
                    header=header,
                    content=section_content,
                    file_path=self._get_relative_path(character_id)
                ))

        return results
