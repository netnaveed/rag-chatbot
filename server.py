import os
import ollama
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from processor import Processor
from chat import Chat

# Initialize Flask app
app = Flask(__name__)

@app.route("/load", methods=["POST"])
def load_api():
    try:
        processor = Processor()
        text = processor.extract_data()
        sections = processor.create_sections(text)
        embeddings = processor.generate_embeddings(sections)
        processor.create_faiss_index(embeddings)
        processor.save_embeddings(sections, embeddings)
        return jsonify({"message": "Content loaded and processed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat_api():
    user_query = request.json.get("query")
    llm = request.json.get("llm", Config.DEFAULT_LLM)

    if not user_query:
        return jsonify({"error": "Query is required."}), 400

    try:
        chat = Chat()
        result = chat.generate_response(user_query, llm)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Handles the /upload endpoint to upload a file to the source directory.
    Only allows specific file formats defined in the config.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Inline file extension check
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in Config.SUPPORTED_FILE_FORMATS:
        filename = secure_filename(file.filename)
        file.save(os.path.join(Config.SOURCE_PATH, filename))
        return jsonify({"message": "File uploaded successfully!"}), 200
    else:
        return jsonify({"error": "Unsupported file format"}), 400
    
@app.route("/files", methods=["GET"])
def list_uploaded_files():
    """
    Lists all files available in the source folder (uploaded content).
    """
    try:
        files = os.listdir(Config.SOURCE_PATH)
        # Optionally, filter to show only supported files
        supported_files = [
            f for f in files
            if any(f.lower().endswith(ext.lower()) for ext in Config.SUPPORTED_FILE_FORMATS)
        ]
        return jsonify({"files": supported_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/clear", methods=["DELETE"])
def clear_source_folder():
    try:
        deleted_files = []

        for filename in os.listdir(Config.SOURCE_PATH):
            file_path = os.path.join(Config.SOURCE_PATH, filename)

            if os.path.isfile(file_path):
                extension = os.path.splitext(filename)[1].lower().lstrip(".")
                if extension in Config.SUPPORTED_FILE_FORMATS:
                    os.remove(file_path)
                    deleted_files.append(filename)

        return jsonify({
            "message": "Supported files deleted successfully.",
            "deleted_files": deleted_files
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/delete_processed", methods=["DELETE"])
def delete_processed():
    """
    Deletes the processed files (text, sections, embeddings, faiss index)
    as per the file paths defined in the config.
    """
    try:
        # List of files to delete
        files_to_delete = [
            Config.TEXT_FILE,
            Config.SECTIONS_FILE,
            Config.FAISS_INDEX_FILE,
            Config.EMBEDDINGS_FILE
        ]
        
        # Attempt to delete each file
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
        
        return jsonify({"message": "Processed files deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/models", methods=["GET"])
def list_models():
    """
    Lists all available LLM models from Ollama.
    """
    try:
        models_response = ollama.list()
        # models_response is a dictionary with a key 'models' that contains a list of dicts
        models = models_response.get("models", [])
        model_names = [model.get("model") for model in models if "model" in model]
        return jsonify({"models": model_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
