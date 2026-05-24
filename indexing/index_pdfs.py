import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

GEMINI_KEY = "AIzaSyBg5bOu3COhHeYA3hBNc0_0MI8QMd-aeNU"
PDF_DIR    = "data/pdfs"
CHROMA_DIR = "data/chroma"
COLLECTION = "policy_docs"


def index_all_pdfs():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GEMINI_KEY,
    )

    # Connect to ChromaDB (creates it if doesn't exist)
    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs: {pdf_files}")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        print(f"\nIndexing: {pdf_file}")

        loader = PyPDFLoader(pdf_path)
        pages  = loader.load()
        chunks = splitter.split_documents(pages)

        # Tag each chunk with its source file for traceability
        for chunk in chunks:
            chunk.metadata["source_file"] = pdf_file

        vectorstore.add_documents(chunks)
        print(f"Stored {len(chunks)} chunks from {pdf_file}")

    total = vectorstore._collection.count()
    print(f"\nDone! Total chunks in ChromaDB: {total}")


if __name__ == "__main__":
    index_all_pdfs()
