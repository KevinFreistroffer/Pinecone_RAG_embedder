import os
from dotenv import load_dotenv
from dataset_processors.PDFProcessor import PDFProcessor
from pinecone_utils.upsert_to_pinecone import upsert_to_pinecone

load_dotenv()


def main():
    try:
        dataset_file_name = "World-Education-Statistics-2024.pdf"
        namespace = "world_education_statistics_2024"
        pdf = PDFProcessor(dataset_file_name)
        pdf.run_process()
        pinecone_records = pdf.get_pinecone_records()
        print("pinecone_records", pinecone_records)
        # print("embeddings", embeded_text_content)
        results = upsert_to_pinecone(
            dataset_file_name=dataset_file_name,
            records=pinecone_records,
            namespace=namespace,
        )
        print("upserted records successfully")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
