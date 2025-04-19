import ollama
from processor import Processor
from config import Config

class Chat:

    def __init__(self):
        self.processor = Processor()
    
    def generate_response(self, user_query, llm):

        # Retrieve the most relevant section using FAISS
        results = self.processor.search(user_query, Config.DEFAULT_TOP_K_RESULTS)
        
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