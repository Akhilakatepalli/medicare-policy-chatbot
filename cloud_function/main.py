import functions_framework
import tempfile
import os
from google.cloud import storage
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma

PROJECT_ID   = "mongodb-gke-project"
CHROMA_DIR   = "/tmp/chroma"
COLLECTION   = "policy_docs"


@functions_framework.cloud_event
def index_pdf(cloud_event):
    data     = cloud_event.data
    bucket   = data["bucket"]
    filename = data["name"]

    if not filename.endswith(".pdf"):
        print(f"Skipping non-PDF file: {filename}")
        return

    print(f"Indexing: gs://{bucket}/{filename}")

    # Download PDF from GCS to temp file
    storage_client = storage.Client()
    blob = storage_client.bucket(bucket).blob(filename)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        blob.download_to_filename(tmp.name)
        tmp_path = tmp.name

    # Load and chunk PDF
    loader   = PyPDFLoader(tmp_path)
    pages    = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(pages)

    # Add source metadata to each chunk
    for chunk in chunks:
        chunk.metadata["source_file"] = filename

    print(f"Created {len(chunks)} chunks from {filename}")

    # Embed and store in ChromaDB
    embeddings = VertexAIEmbeddings(
        model_name="textembedding-gecko@003",
        project=PROJECT_ID,
    )
    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    vectorstore.add_documents(chunks)

    print(f"Successfully indexed {filename} — {len(chunks)} chunks stored in ChromaDB")
    os.unlink(tmp_path)
