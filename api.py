from flask import Flask, request, jsonify
from chatbot import Chatbot
from data_processor import DataProcessor
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Initialize Chatbot and DataProcessor
data_processor = DataProcessor()
chatbot = Chatbot()

@app.route("/load", methods=["POST"])
def load_data():
    try:
        message = data_processor.process_data()
        chatbot.embedding_generator.load_faiss_index()
        chatbot.embedding_generator.load_embeddings()
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    llm = request.json.get("llm", Config.DEFAULT_LLM)
    result = chatbot.generate_response(user_query, llm)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
