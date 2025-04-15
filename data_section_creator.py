import os
import nltk
from config import Config

# Ensure NLTK punkt tokenizer is available
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class SectionCreator:

    def __init__(self):
        self.sections_output = os.path.join(Config.PROCESSED_PATH, "sections.txt")

    def create_sections(self, text, max_chars=Config.SECTION_LENGTH, overlap=Config.SECTION_OVERLAP):
        """Splits text into overlapping sections based on sentences for better context retention."""
        sentences = sent_tokenize(text)
        sections = []
        current_section = ""

        for sentence in sentences:
            if len(current_section) + len(sentence) <= max_chars:
                current_section += " " + sentence
            else:
                sections.append(current_section.strip())
                # Add overlap from end of previous section
                overlap_text = " ".join(current_section.strip().split()[-(overlap // 10):])
                current_section = overlap_text + " " + sentence

        if current_section:
            sections.append(current_section.strip())

        # Save sections
        with open(self.sections_output, "w", encoding="utf-8") as output_file:
            for section in sections:
                output_file.write(section + "\n###\n")

        return sections
