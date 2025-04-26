from sentence_transformers import SentenceTransformer
import os
from PyPDF2 import PdfReader

# from DatasetProcessors._BaseProcessor import _BaseProcessor
from pinecone_utils.upsert_to_pinecone import upsert_to_pinecone

# TODO implement a BaseProcessor requiring these method names?
class PDFProcessor:
    def __init__(self, file_name):
        print("Initializing PDFProcessor...")
        if not file_name:
            raise ValueError("File name is required")
        try:
            self.file_name = file_name
            print(f"Loading sentence transformer model for file: {file_name}")
            self.model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
            self.text_content = []
            self.embedded_text_content = []
            self.pinecone_records = []
            print("PDFProcessor initialized successfully")
        except Exception as e:
            print(f"Error initializing PDFProcessor: {e}")
            raise

    def get_reader(self):
        print("Getting PDF reader...")
        root_dir = os.path.dirname(os.path.dirname(__file__))
        pdf_path = os.path.join(root_dir, "data_files", self.file_name)
        print(f"Attempting to read PDF from: {pdf_path}")
        reader = PdfReader(pdf_path)
        print("PDF reader obtained successfully")
        return reader

    def extract_and_store_text_content(self):
        print("Starting text extraction from PDF...")
        reader = self.get_reader()
        i = 0
        for page in reader.pages:
            print(f"Processing page {i}...")
            self.text_content.append(page.extract_text())
            i += 1
        print(f"Completed text extraction. Total pages processed: {i}")

    def convert_text_to_embeddings(self):
        print("Starting text embedding process...")
        text_content = self.text_content

        if len(text_content) == 0:
            print("No text content to process")
            return

        print("Encoding text content...")
        self.embedded_text_content = self.model.encode(text_content)
        print("Embedded text content generated successfully")

    def get_text_content(self):
        print("Retrieving text content...")
        return self.text_content

    def get_embeded_text_content(self):
        print("Retrieving embedded text content...")
        return self.embedded_text_content

    def get_pinecone_records(self):
        print("Retrieving Pinecone records...")
        return self.pinecone_records

    def prepare_records_for_upsert(self):
        print("Preparing records for Pinecone upsert...")

        if len(self.embedded_text_content) == 0:
            print("No embeddings generated")
            raise ValueError("No embeddings to upsert")

        print("Structuring embeddings for upsert...")
        self.pinecone_records = []

        for index, (original_text, embedding) in enumerate(
            zip(self.text_content, self.embedded_text_content)
        ):
            record = {
                "id": str(index),
                "values": embedding,
                "metadata": {"original_text": original_text},
            }
            self.pinecone_records.append(record)

        print(f"Prepared {len(self.pinecone_records)} records for Pinecone upsert")

    def run_process(self):
        print("Starting PDF processing pipeline...")
        self.extract_and_store_text_content()
        self.convert_text_to_embeddings()
        self.prepare_records_for_upsert()
        print("PDF processing completed")
