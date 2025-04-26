import os
from dotenv import load_dotenv
from pinecone import Pinecone as PC, ServerlessSpec
from PyPDF2 import PdfReader
import numpy as np

load_dotenv()

# API Keys for various services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not set.")


class PineconeUtils:
    def __init__(self):
        self.pc = PC(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index("rag-768")

    def upsert_docs(self, records, namespace):
        print("Pinecone.upserting docs...", namespace)

        try:
            if records is None or len(records) == 0:
                raise ValueError("Records array is empty.")

            # Batch size to stay under 2MB limit
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                print(
                    f"Upserting batch {i//batch_size + 1} of {(len(records) + batch_size - 1)//batch_size}"
                )
                self.index.upsert(
                    vectors=batch, namespace=namespace if namespace else "ns1"
                )

            print("Successfully upserted all documents")
        except Exception as e:
            print(f"Error upserting documents: {e}")
            raise
