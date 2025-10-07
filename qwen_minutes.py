import httpx
import os

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Prefer env var for security; default placeholder for quickstart
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")
YOUR_SITE_URL = os.getenv("APP_SITE_URL", "https://your-app.com")  # optional, for attribution
YOUR_APP_NAME = os.getenv("APP_NAME", "MeetingMinutesApp")          # optional


def call_qwen(prompt: str, system_message: str) -> str:
    response = httpx.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_APP_NAME,
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen-1.5-72b-chat",  # or "qwen/qwen-72b-chat"
            "temperature": 0.0,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


# --- Extraction Functions ---
def abstract_summary_extraction(transcription: str) -> str:
    system_msg = (
        "You are a highly skilled AI trained in language comprehension and summarization. "
        "Read the following meeting transcript and summarize it into a concise abstract paragraph. "
        "Retain the most important points, avoid unnecessary details, and ensure clarity."
    )
    return call_qwen(transcription, system_msg)


def key_points_extraction(transcription: str) -> str:
    system_msg = (
        "You are an expert at distilling conversations into key points. "
        "From the transcript below, extract 3–7 main discussion points that capture the essence of the meeting. "
        "Present them as a numbered or bulleted list."
    )
    return call_qwen(transcription, system_msg)


def action_item_extraction(transcription: str) -> str:
    system_msg = (
        "You are an AI that identifies tasks and responsibilities from meetings. "
        "Review the transcript and list all action items: who is responsible for what, and by when (if mentioned). "
        "Format as a clear list with assignees and deadlines where possible."
    )
    return call_qwen(transcription, system_msg)


def sentiment_analysis(transcription: str) -> str:
    system_msg = (
        "Analyze the overall sentiment of this meeting transcript. "
        "Is the tone positive, neutral, or negative? Consider collaboration, urgency, satisfaction, or frustration. "
        "Provide a short paragraph with your reasoning."
    )
    return call_qwen(transcription, system_msg)


# --- Main function ---
def meeting_minutes(transcription: str) -> dict:
    return {
        "abstract_summary": abstract_summary_extraction(transcription),
        "key_points": key_points_extraction(transcription),
        "action_items": action_item_extraction(transcription),
        "sentiment": sentiment_analysis(transcription),
    }

