from flask import Flask, request, jsonify
from chatbot import Chatbot
from config import Config
from data_extractor import DataExtractor
from data_section_creator import SectionCreator
from data_embedding_generator import EmbeddingGenerator

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbot
chatbot = Chatbot()

def load_data():
    """Handles the /load endpoint to process data, create sections, and save embeddings."""
    try:
        # Data extraction and processing logic
        extractor = DataExtractor()
        section_creator = SectionCreator()
        embedding_generator = EmbeddingGenerator()

        text = extractor.extract_data()
        sections = section_creator.create_sections(text)
        embeddings = embedding_generator.generate_embeddings(sections)
        embedding_generator.create_faiss_index(embeddings)
        embedding_generator.save_embeddings(sections, embeddings)

        # Reload FAISS index and embeddings for the chatbot
        chatbot.embedding_generator.load_faiss_index()
        chatbot.embedding_generator.load_embeddings()

        return jsonify({"message": "Content loaded and processed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def chat():
    """Handles the /chat endpoint to generate a response based on user query."""
    # Extract user query and LLM model from request
    user_query = request.json.get("query")
    llm = request.json.get("llm", Config.DEFAULT_LLM)

    # Validate the query input
    if not user_query:
        return jsonify({"error": "Query is required."}), 400
    
    # Generate the chatbot response
    try:
        result = chatbot.generate_response(user_query, llm)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define the API routes
@app.route("/load", methods=["POST"])
def load_api():
    return load_data()

@app.route("/chat", methods=["POST"])
def chat_api():
    return chat()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
