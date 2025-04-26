import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from DatasetProcessors.PDFProcessor import PDFProcessor
from utils.decorators.decorators import log_function
from utils.PineconeUtils import PineconeUtils
from pinecone_utils.upsert_to_pinecone import upsert_to_pinecone

load_dotenv()

# API Keys for various services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise "Pinecone API key not set."


@log_function
def main():
    try:
        dataset_file_name = "World-Education-Statistics-2024.pdf"
        namespace = "world_education_statistics_2024"
        pdf = PDFProcessor(dataset_file_name)
        pdf.run_process()
        # text_content = pdf.get_text_content()
        # embeded_text_content = pdf.get_embeded_text_content()
        pinecone_records = pdf.get_pinecone_records()
        print("pinecone_records", pinecone_records)
        # print("embeddings", embeded_text_content)
        results = upsert_to_pinecone(
            dataset_file_name=dataset_file_name, 
            records=pinecone_records, 
            namespace=namespace
        )
        print("upserted records successfully")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
