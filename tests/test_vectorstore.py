from utils.vectorestore import create_vector_store


def test_vector_store_search() -> None:
    chunks = ["The capital of France is Paris", "The capital of Germany is Berlin"]
    store = create_vector_store(chunks)

    results = store.similarity_search("What is the capital of France?", k=1)
    assert "Paris" in results[0].page_content