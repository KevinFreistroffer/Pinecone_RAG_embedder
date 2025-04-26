import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not set.")

pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index("rag-768")

def upsert_to_pinecone(dataset_file_name, records, namespace):
    print("Pinecone.upserting records...", namespace)

    try:
        # records = []
        # for index, (original_text, embeded_text) in enumerate(zip(text_content, embeded_text_content)):
        #     record = {
        #         "id": str(index),
        #         "values": embeded_text,
        #         "metadata": {
        #             "original_text": original_text
        #         }
        #     }
        #     records.append(record)
  
        if records is None or len(records) == 0:
            raise ValueError("Records array is empty.")

        # Batch size to stay under 2MB limit
        batch_size = 100
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            print(
                f"Upserting batch {i//batch_size + 1} of {(len(records) + batch_size - 1)//batch_size}"
            )
            pinecone_index.upsert(
                vectors=batch, namespace=namespace if namespace else dataset_file_name
            )

        print(f"Successfully upserted all {len(records)} records")
    except Exception as e:
        print(f"Error upserting records: {e}")
        raise
