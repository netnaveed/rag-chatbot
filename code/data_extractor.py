import os
import fitz  # PyMuPDF for PDFs
from docx import Document
from config import Config

class DataExtractor:

    def __init__(self):
        self.source_path = Config.SOURCE_PATH
        self.processed_path = Config.PROCESSED_PATH
        self.text_output = os.path.join(self.processed_path, "text.txt")

    def extract_data(self):
        
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Base path not found: {self.source_path}")

        extracted_texts = []

        for file_name in os.listdir(self.source_path):
            file_path = os.path.join(self.source_path, file_name)

            if file_name.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            elif file_name.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            elif file_name.endswith(".pdf"):
                pdf_doc = fitz.open(file_path)
                text = "\n".join([page.get_text("text") for page in pdf_doc])
            else:
                continue  # Skip unsupported files

            if text.strip():
                extracted_texts.append(f"### Extracted from {file_name} ###\n{text}\n")

        if not extracted_texts:
            raise ValueError("No valid text content found in the given documents.")

        full_text = "\n".join(extracted_texts)

        # Save extracted text
        with open(self.text_output, "w", encoding="utf-8") as output_file:
            output_file.write(full_text)

        return full_text
