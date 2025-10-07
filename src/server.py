from flask import Flask, request, jsonify
import tempfile
import os
from pathlib import Path

from transcribe import transcribe_audio
from qwen_minutes import meeting_minutes

# Serve static files from project root so frontend and API run on same host
BASE_DIR = Path(__file__).resolve().parents[1]
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path='')


@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    """Accepts multipart file upload (field 'file') and returns a transcription."""
    if "file" not in request.files:
        return jsonify({"error": "missing file field"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400

    # Save to a temp file and call the existing transcribe_audio helper
    suffix = Path(f.filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name

    try:
        text = transcribe_audio(tmp_path)
        # transcribe_audio currently returns text only; wrap for future expansion
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


@app.route("/api/minutes", methods=["POST"])
def api_minutes():
    """Generate structured minutes from a transcript. Expects JSON { transcript, template }"""
    data = request.get_json(force=True)
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"error": "missing transcript"}), 400

    try:
        minutes = meeting_minutes(transcript)
        return jsonify(minutes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files from the repo root (index.html, app.js, styles.css)."""
    # Security: only serve known static extensions
    allowed_ext = {'.html', '.js', '.css', '.png', '.svg', '.ico', '.json'}
    target = BASE_DIR / path
    if target.exists() and target.suffix in allowed_ext:
        return app.send_static_file(path)
    # Fallback to index.html for client-side routing
    return app.send_static_file('index.html')


if __name__ == "__main__":
    # For local development only
    app.run(host="0.0.0.0", port=8000, debug=True)
