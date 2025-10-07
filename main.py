from transcribe import transcribe_audio
from qwen_minutes import meeting_minutes
from export_docx import save_as_docx


if __name__ == "__main__":
    AUDIO_FILE = "meeting_recording.mp3"  # your audio file

    print("🎙 Transcribing audio...")
    transcript = transcribe_audio(AUDIO_FILE)
    print(" Transcription complete.")

    print("🧠 Generating meeting minutes with Qwen...")
    minutes = meeting_minutes(transcript)
    print(" Minutes generated.")

    print("📄 Saving to Word document...")
    save_as_docx(minutes, "meeting_minutes.docx")
    print(" Saved as 'meeting_minutes.docx'")

