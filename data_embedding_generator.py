import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config


class EmbeddingGenerator:
    
    def __init__(self):
        self.processed_path = Config.PROCESSED_PATH
        self.faiss_index_path = os.path.join(self.processed_path, "faiss.index")
        self.embeddings_path = os.path.join(self.processed_path, "embeddings.pkl")
        self.model = SentenceTransformer(Config.DEFAULT_SENTENCE_TRANSFORMER_MODEL)
        self.index = None
        self.sections = []
        self.load_faiss_index()
        self.load_embeddings()

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

    def search(self, query, top_k=5):
        """Finds the most similar sections to the given query."""
        if self.index is None or len(self.sections) == 0:
            return []
        
        query_embedding = self.generate_embeddings([query])
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = [(self.sections[i], distances[0][j]) for j, i in enumerate(indices[0]) if i < len(self.sections)]
        return results
