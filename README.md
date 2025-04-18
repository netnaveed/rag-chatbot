# RAG-Based Chatbot
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
- Run this in terminal to pull required models:
```bash
ollama pull mistral
ollama pull llama2
ollama pull your-custom-model-name
```
- Make sure Ollama is running in the background before you start the chatbot.

### Installation of required python packages
```bash
python install_requirements.py
```

### Start API Server
```bash
python api.py
```

### Start Chatbot Web UI
```bash
streamlit run web.py
```

### APIs
- Load Content: GET http://127.0.0.1:5000/load
- Ask a Question: POST http://127.0.0.1:5000/chat