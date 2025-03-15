from data_extractor import DataExtractor
from data_section_creator import SectionCreator
from data_embedding_generator import EmbeddingGenerator

class DataProcessor:

    def __init__(self):
        self.extractor = DataExtractor()
        self.section_creator = SectionCreator()
        self.embedding_generator = EmbeddingGenerator()

    def process_data(self):
        try:
            text = self.extractor.extract_data()
            sections = self.section_creator.create_sections(text)
            embeddings = self.embedding_generator.generate_embeddings(sections)
            self.embedding_generator.create_faiss_index(embeddings)
            self.embedding_generator.save_embeddings(sections, embeddings)
            return "Content loaded and processed successfully!"
        except Exception as e:
            return {"error": str(e)}
