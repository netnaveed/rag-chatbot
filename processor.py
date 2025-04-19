import os
import ollama
import pickle
import faiss
import fitz
import numpy as np
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from docx import Document
from config import Config

class Processor:
    
    def __init__(self):
        self.source_path = Config.SOURCE_PATH
        self.processed_path = Config.PROCESSED_PATH
        self.text_output = Config.TEXT_FILE
        self.sections_output = Config.SECTIONS_FILE
        self.faiss_index_path = Config.FAISS_INDEX_FILE
        self.embeddings_path = Config.EMBEDDINGS_FILE
        self.model = SentenceTransformer(Config.DEFAULT_SENTENCE_TRANSFORMER_MODEL)
        self.index = None
        self.sections = []
        self.load_faiss_index()
        self.load_embeddings()

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

    def create_sections(self, text, max_chars=Config.DEFAULT_SECTION_LENGTH, overlap=Config.DEFAULT_SECTION_OVERLAP):
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

    def generate_embeddings(self, sections):
        """Encodes text sections into vector embeddings."""
        embeddings = self.model.encode(sections, convert_to_tensor=True)
        return np.array([embedding.cpu().numpy() for embedding in embeddings])

    def create_faiss_index(self, embeddings):
        """Creates and saves a FAISS index."""
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        faiss.write_index(self.index, self.faiss_index_path)
        return self.index

    def save_embeddings(self, sections, embeddings):
        """Saves sections and embeddings for later use."""
        with open(self.embeddings_path, "wb") as output_file:
            pickle.dump((sections, embeddings), output_file)

    def load_faiss_index(self):
        """Loads the FAISS index if it exists."""
        if os.path.exists(self.faiss_index_path):
            self.index = faiss.read_index(self.faiss_index_path)
        else:
            self.index = None

    def load_embeddings(self):
        """Loads stored embeddings and sections if available."""
        if os.path.exists(self.embeddings_path):
            with open(self.embeddings_path, "rb") as input_file:
                self.sections, _ = pickle.load(input_file)

    def search(self, query, top_k):
        """Finds the most similar sections to the given query."""
        if self.index is None or len(self.sections) == 0:
            return []
        
        query_embedding = self.generate_embeddings([query])
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = [(self.sections[i], distances[0][j]) for j, i in enumerate(indices[0]) if i < len(self.sections)]
        return results
    
    def generate_response(self, user_query, llm):
        # Retrieve the most relevant section using FAISS
        results = self.search(user_query, Config.DEFAULT_TOP_K_RESULTS)
        
        if not results:
            return {
                "query": user_query,
                "response": Config.NO_INFORMATION_RESPONSE
            }
        
        relevant_section, _ = results[0]
        
        # Generate AI response using LLM
        response = ollama.chat(
            model=llm,
            messages=[
                {"role": "system", "content": Config.SYSTEM_MESSAGE},
                {"role": "system", "content": f"Content: {relevant_section}"},
                {"role": "user", "content": user_query}
            ]
        )
        
        return {
            "query": user_query, 
            "response": response['message']['content'].strip(),
            "relevant_sections": relevant_section
        }
