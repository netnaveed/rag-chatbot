import os

class Config:
    
    DEBUG                               = True
    BASE_DIR                            = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    SOURCE_PATH                         = os.path.join(BASE_DIR, "source")
    PROCESSED_PATH                      = os.path.join(BASE_DIR, "processed")
    TEXT_FILE                           = os.path.join(PROCESSED_PATH, "text.txt")
    SECTIONS_FILE                       = os.path.join(PROCESSED_PATH, "sections.txt")
    FAISS_INDEX_FILE                    = os.path.join(PROCESSED_PATH, "faiss.index")
    EMBEDDINGS_FILE                     = os.path.join(PROCESSED_PATH, "embeddings.pkl")
    DEFAULT_SECTION_LENGTH              = 500
    DEFAULT_SECTION_OVERLAP             = 100
    DEFAULT_TOP_K_RESULTS               = 5
    SUPPORTED_FILE_FORMATS              = {"txt", "docx", "pdf"}
    DEFAULT_SENTENCE_TRANSFORMER_MODEL  = "sentence-transformers/all-mpnet-base-v2"
    DEFAULT_LLM                         = "mistral"
    NO_INFORMATION_RESPONSE             = "I'm sorry, but I don't have enough information to answer that."
    SYSTEM_MESSAGE                      = "Based on the following information, answer the user's question in a complete and informative sentence."