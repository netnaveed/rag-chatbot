# RAG Chatbot
A locally deployed AI-powered chatbot that uses Retrieval-Augmented Generation (RAG) for accurate, context-aware responses based on your own documents.

## Features
- Extracts text from uploaded documents
- Splits content into sections
- Generates embeddings using Sentence Transformers
- Uses FAISS for fast similarity search
- Leverages LLM (like Mistral via Ollama) for generating responses

## Getting Started

### Ollama & LLM Setup
- Install Ollama: https://ollama.com/download
- Run in terminal to pull required models:
```bash
ollama pull mistral
ollama pull llama2
ollama pull your-custom-model-name
```
- Make sure Ollama is running in the background before you start the chatbot.

### Install required Python packages and verify other installations.
```bash
pip install -r requirements.txt
python requirements_check.py
```
### Start API Server
```bash
python main.py
```
### APIs
- Upload document: POST http://127.0.0.1:5000/documents/upload
- Process documents: POST http://127.0.0.1:5000/documents/process
- Delete documents and embeddings: DELETE http://127.0.0.1:5000/documents/clear
- Chat with chatbot: POST http://127.0.0.1:5000/chat