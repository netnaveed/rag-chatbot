import os

class Config:
    
    DEBUG                               = True
    BASE_DIR                            = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    SOURCE_PATH                         = os.path.join(BASE_DIR, "data", "source")
    PROCESSED_PATH                      = os.path.join(BASE_DIR, "data", "processed")
    SUPPORTED_FILE_FORMATS              = {"pdf", "txt", "docx"}

    TEXT_FILE                           = os.path.join(PROCESSED_PATH, "text.txt")
    SECTIONS_FILE                       = os.path.join(PROCESSED_PATH, "sections.txt")
    FAISS_INDEX_FILE                    = os.path.join(PROCESSED_PATH, "faiss.index")
    EMBEDDINGS_FILE                     = os.path.join(PROCESSED_PATH, "embeddings.pkl")

    DEFAULT_SECTION_LENGTH              = 500
    DEFAULT_SECTION_OVERLAP             = 100
    DEFAULT_SENTENCE_TRANSFORMER_MODEL  = "sentence-transformers/all-mpnet-base-v2"
    TOP_K_RESULTS                       = 1
    DEFAULT_LLM                         = "llama3.2" # mistral, deepseek-r1, llama3.2

    NO_INFORMATION_RESPONSE             = "I'm sorry, but I don't have enough information to answer that."
    SYSTEM_MESSAGE                      = "Based on the following information, answer the user's question in a complete and informative sentence."