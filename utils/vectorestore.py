import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embedding_model() -> HuggingFaceEmbeddings:
    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    return HuggingFaceEmbeddings(model_name=model_name)


def create_vector_store(chunks: list[str]) -> VectorStore:
    """
    Convert chunks into vectors and store them in an in-memory ChromaDB
    """
    embeddings = get_embedding_model()
    COLLECTION_NAME = "youtube_transcript"

    try:
        old_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )
        old_store.delete_collection()

    except Exception:
        pass

    vectore_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vectore_store