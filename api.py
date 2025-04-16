from flask import Flask, request, jsonify
from config import Config
from data_embedding_generator import EmbeddingGenerator
from chatbot_manager import ChatbotManager

# Initialize Flask app
app = Flask(__name__)

# Initialize ChatbotManager
chatbot_manager = ChatbotManager()

@app.route("/load", methods=["POST"])
def load_api():
    """
    Handles the /load endpoint to process data, create sections,
    generate and save embeddings, and reload chatbot.
    """
    try:
        embedding_generator = EmbeddingGenerator()

        text = embedding_generator.extract_data()
        sections = embedding_generator.create_sections(text)
        embeddings = embedding_generator.generate_embeddings(sections)
        embedding_generator.create_faiss_index(embeddings)
        embedding_generator.save_embeddings(sections, embeddings)

        # Reload the chatbot to pick up updated index and sections
        chatbot_manager.reload_chatbot()

        return jsonify({"message": "Content loaded and processed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat_api():
    """
    Handles the /chat endpoint to generate a response using the chatbot.
    """
    user_query = request.json.get("query")
    llm = request.json.get("llm", Config.DEFAULT_LLM)

    if not user_query:
        return jsonify({"error": "Query is required."}), 400

    try:
        chatbot = chatbot_manager.get_chatbot()
        result = chatbot.generate_response(user_query, llm)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
