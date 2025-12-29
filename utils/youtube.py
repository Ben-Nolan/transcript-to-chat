import re
from typing import NamedTuple

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import TextFormatter


class TranscriptResponse(NamedTuple):
    text: str
    metadata: str

def extract_video_id(url: str) -> str:
    """
    Robustly extracts the video ID from various YouTube URL formats.
    """
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    
    if match is None:
        raise ValueError(f"Invalid Youtube URL(no video is found): {url}")
    else:
        return match.group(1)


def get_transcript_text(url: str) -> TranscriptResponse:
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid Youtube URL provided.")

    yt = YouTubeTranscriptApi()

    try:
        transcript_list = yt.list(video_id)
        transcript = None
        transcript_type = ""

        try:
            # Attempt to find a manually created English transcript (Highest Quality)
            transcript = transcript_list.find_manually_created_transcript(['en'])
            transcript_type = "manual english subtitles (high quality)"

        except NoTranscriptFound:
            try:
                # Attempt to find an auto-generated English transcript (Medium Quality)
                transcript = transcript_list.find_generated_transcript(['en'])
                transcript_type = "auto-generated english subtitles (medium quality)"

            except NoTranscriptFound:
                # Pull a transcript in any language and translate it into english
                # Get the first avaialable transcript regardless of language
                for t in transcript_list:
                    transcript = t.translate("en")
                    transcript_type = (
                        f"{t.language} translated to english (low quality)"
                    )
                    break

        if not transcript:
            raise RuntimeError(f"No transcript available for {video_id}")

        transcript_data = transcript.fetch()

        formatter = TextFormatter()
        transcript_formatted = (formatter.format_transcript(transcript_data)
                                         .replace("\n", " "))
        return TranscriptResponse(text=transcript_formatted, metadata=transcript_type)


    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise RuntimeError(f"Transcript unavailable: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected system failure: {str(e)}")