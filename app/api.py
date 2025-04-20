import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from .config import Config
from .processor import Processor

# Initialize Flask app
app = Flask(__name__)

@app.route("/documents/upload", methods=["POST"])
def upload_file():
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

@app.route("/documents/process", methods=["POST"])
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
    
@app.route("/documents/clear", methods=["DELETE"])
def clear_files():
    content_type = request.args.get("content", "all").lower()

    deleted_source_files = []
    deleted_processed_files = []

    try:
        if content_type in ["source", "all"]:
            for filename in os.listdir(Config.SOURCE_PATH):
                file_path = os.path.join(Config.SOURCE_PATH, filename)
                if os.path.isfile(file_path):
                    extension = os.path.splitext(filename)[1].lower().lstrip(".")
                    if extension in Config.SUPPORTED_FILE_FORMATS:
                        os.remove(file_path)
                        deleted_source_files.append(filename)

        if content_type in ["processed", "all"]:
            processed_files = [
                Config.TEXT_FILE,
                Config.SECTIONS_FILE,
                Config.FAISS_INDEX_FILE,
                Config.EMBEDDINGS_FILE
            ]
            for file_path in processed_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_processed_files.append(os.path.basename(file_path))

        return jsonify({
            "message": "Files deleted successfully.",
            "deleted_source_files": deleted_source_files,
            "deleted_processed_files": deleted_processed_files
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_query = request.json.get("query")
        llm = request.json.get("llm", Config.DEFAULT_LLM)

        if not user_query:
            return jsonify({"error": "Query is required."}), 400

        processor = Processor()
        result = processor.generate_response(user_query, llm)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
