import ollama
from data_processor import DataProcessor
from config import Config

class Chatbot:

    def __init__(self):

        self.source_path = Config.SOURCE_PATH
        self.data_processor = DataProcessor()
        self.index = self.data_processor.index
        self.sections = self.data_processor.sections
    
    def generate_response(self, user_query, llm):

        if self.index is None or not self.sections:
            return {
                "error": "Embeddings not found."
            }
        
        # Retrieve the most relevant section using FAISS
        results = self.data_processor.search(user_query, top_k=1)
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
            "relevant_section": relevant_section
        }
