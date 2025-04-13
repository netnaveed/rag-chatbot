# Chatbot

A locally deployed AI-powered chatbot that uses Retrieval-Augmented Generation (RAG) for accurate, context-aware responses based on your own documents.

## Features

- Extracts text from uploaded documents
- Splits content into sections
- Generates embeddings using Sentence Transformers
- Uses FAISS for fast similarity search
- Leverages LLM (like Mistral via Ollama) for generating responses

## Getting Started

### Start API Server

```bash
python api.py
```

### APIs

- Load Content: GET http://127.0.0.1:5000/load
- Ask a Question: POST http://127.0.0.1:5000/chat

### Start Chatbot Web UI

```bash
streamlit run web.py
```