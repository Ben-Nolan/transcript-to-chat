from typing import Any
from unittest.mock import MagicMock, patch

from utils.llm import get_rag_chain


@patch("utils.llm.ChatGroq")
def test_get_rag_chain_structure(mock_chat_groq: Any) -> None:
    mock_vector_store = MagicMock()
    mock_vector_store.as_retriever.return_value = MagicMock()

    chain = get_rag_chain(mock_vector_store, k_chunks=3)

    assert chain is not None
    assert hasattr(chain, "invoke")

@patch("utils.llm.ChatGroq")
def test_chain_execution_mock(mock_chat_groq: Any) -> None:
    mock_llm_instance = mock_chat_groq.return_value
    mock_llm_instance.invoke.return_value = MagicMock(content="This is a test answer")

    mock_vector_store = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "The sky is blue."
    (mock_vector_store.as_retriever
                      .return_value
                      .get_relevant_documents
                      .return_value) = [mock_doc]

    chain = get_rag_chain(mock_vector_store, k_chunks=3)

    assert chain is not None