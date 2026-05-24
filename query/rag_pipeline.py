import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

PROJECT_ID  = "mongodb-gke-project"
CHROMA_DIR  = "data/chroma"
COLLECTION  = "policy_docs"
GEMINI_KEY  = os.getenv("GEMINI_API_KEY", "AIzaSyBg5bOu3COhHeYA3hBNc0_0MI8QMd-aeNU")  # env var injected by k8s Secret in GKE

PROMPT_TEMPLATE = """
You are a Medicare and Medicaid policy expert assistant for hospital billing staff and fraud investigators.
Answer ONLY based on the policy documents provided below.
If the answer is not in the documents, say "I could not find this information in the policy documents."
Always mention the source document and relevant billing codes when available.

Policy Documents:
{context}

Question: {question}

Answer:
"""


def get_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GEMINI_KEY,
    )
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def get_rag_chain():
    vectorstore = get_vectorstore()
    retriever   = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_KEY,
        temperature=0,
        max_output_tokens=1024,
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask(question: str) -> dict:
    chain, retriever = get_rag_chain()
    answer  = chain.invoke(question)
    sources = list(set(
        doc.metadata.get("source_file", "unknown")
        for doc in retriever.invoke(question)
    ))

    return {
        "question": question,
        "answer":   answer,
        "sources":  sources,
    }


if __name__ == "__main__":
    questions = [
        "Does Medicare cover telehealth services?",
        "What is the billing code for a CPAP machine?",
        "What are the prior authorization requirements for Medicaid?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 60)
