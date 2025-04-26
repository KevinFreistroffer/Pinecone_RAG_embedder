# .env
PINECONE_API_KEY=123

# Cloud Services ideas:

Ingestion & Storage: Upload PDFs into object storage (S3 / Blob Storage / GCS).

Text Extraction: Trigger PDF→text extraction via serverless compute calling Textract / Cognitive Services / Vision API.

Embedding Service: Host your SentenceTransformers model as a managed inference endpoint (SageMaker / Azure ML / Vertex AI).

Vector DB Integration: From that endpoint, call Pinecone (via its client SDK) to upsert embeddings—Pinecone is available in each cloud’s marketplace or via public API.

Orchestration & Monitoring: Wire steps with Step Functions / Logic Apps / Cloud Workflows and monitor with CloudWatch / Monitor / Stackdriver.