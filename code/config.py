import os

class Config:
    BASE_DIR                    = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    SOURCE_PATH                 = os.path.join(BASE_DIR, "data", "source")
    PROCESSED_PATH              = os.path.join(BASE_DIR, "data", "processed")
    SENTENCE_TRANSFORMER_MODEL  = "sentence-transformers/all-mpnet-base-v2"
    SECTION_LENGTH              = 500
    SECTION_OVERLAP             = 100
    LLM_MODEL                   = "mistral"
    DEBUG                       = True