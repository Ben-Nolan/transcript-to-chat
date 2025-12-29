from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.vectorstores import VectorStore
from langchain_groq import ChatGroq


def get_rag_chain(
        vector_store: VectorStore,
        k_chunks: int
    ) -> Runnable[Any, str]:
    """
    Creats a Chain that connects the Vector Store to the Groq LLM
    """
    llm = ChatGroq(
        temperature=0,
        model="llama-3.1-8b-instant"
    )


    template = """
    You are a helpful assistant specialized in analyzing Youtube transcripts.
    Answer the questions based ONLY on the following context:

    {context}

    Question: {question}

    Helpful Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    retriever = vector_store.as_retriever(search_kwargs={"k": k_chunks})

    chain: Runnable[Any, str] = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
