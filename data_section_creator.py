import os
from config import Config

class SectionCreator:

    def __init__(self):
        self.sections_output = os.path.join(Config.PROCESSED_PATH, "sections.txt")

    def create_sections(self, text, max_chars=Config.SECTION_LENGTH, overlap=Config.SECTION_OVERLAP):
        """Splits text into overlapping sections for better context retention."""
        lines = text.split("\n")
        sections = []
        current_section = ""

        for line in lines:
            if len(current_section) + len(line) <= max_chars:
                current_section += " " + line
            else:
                sections.append(current_section.strip())
                current_section = " ".join(current_section.split()[-(overlap // 10):]) + " " + line

        if current_section:
            sections.append(current_section.strip())

        # Save sections
        with open(self.sections_output, "w", encoding="utf-8") as output_file:
            for section in sections:
                output_file.write(section + "\n###\n")

        return sections
