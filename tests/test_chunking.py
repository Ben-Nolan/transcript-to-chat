from utils.chunking import chunk_text


def test_chunk_text_length() -> None:
    text = "This is a long sentence that we want to split"
    chunks = chunk_text(text, 10, 0)

    assert len(chunks) > 1
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")