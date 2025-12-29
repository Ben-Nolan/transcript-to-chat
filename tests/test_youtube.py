import pytest

from utils.youtube import extract_video_id


def test_extract_video_id_valid() -> None:
    """
    Testing various youtube url formats
    """
    standard_url = "https://www.youtube.com/watch?v=pLw-52UPKnU"
    shared_standard_url = "https://youtu.be/pLw-52UPKnU?si=Gbs0kIAnft2pSmPM"
    shorts_url = "https://www.youtube.com/shorts/0TIH4BKvmoU"
    shared_shorts_url = "https://youtube.com/shorts/0TIH4BKvmoU?si=NEFfCaM7W7S-Kl3O"
    mobile_url = "https://m.youtube.com/watch?v=dDXu_vt9gG0&pp=ygUIQmVhc3R5cXTSBwkJTQoBhyohjO8%3D"
    mobile_to_desktop_url = "https://www.youtube.com/watch?app=desktop&v=dDXu_vt9gG0"

    assert extract_video_id(standard_url) == "pLw-52UPKnU"
    assert extract_video_id(shared_standard_url) == "pLw-52UPKnU"
    assert extract_video_id(shorts_url) == "0TIH4BKvmoU"
    assert extract_video_id(shared_shorts_url) == "0TIH4BKvmoU"
    assert extract_video_id(mobile_url) == "dDXu_vt9gG0"
    assert extract_video_id(mobile_to_desktop_url) == "dDXu_vt9gG0"


def test_extract_video_id_invalid() -> None:
    url = "https://www.google.com"
    with pytest.raises(ValueError):
        extract_video_id(url)
