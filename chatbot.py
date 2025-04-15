import ollama
from data_embedding_generator import EmbeddingGenerator
from config import Config

class Chatbot:

    def __init__(self):

        self.source_path = Config.SOURCE_PATH
        self.embedding_generator = EmbeddingGenerator()
        self.index = self.embedding_generator.index
        self.sections = self.embedding_generator.sections
    
    def generate_response(self, user_query):

        if self.index is None or not self.sections:
            return {"error": "Embeddings not found."}
        
        # Retrieve the most relevant section using FAISS
        results = self.embedding_generator.search(user_query, top_k=1)
        if not results:
            return {"query": user_query, "response": Config.NO_INFORMATION_RESPONSE}
        
        relevant_section, _ = results[0]
        
        # Generate AI response using LLM model
        response = ollama.chat(model=Config.LLM_MODEL, messages=[
            {"role": "system", "content": Config.SYSTEM_MESSAGE},
            {"role": "system", "content": f"Content: {relevant_section}"},
            {"role": "user", "content": user_query}
        ])
        
        return {
            "query": user_query, 
            "response": response['message']['content'].strip(),
            "relevant_section": relevant_section
        }
