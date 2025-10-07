"""
Connectivity check for Qwen using env-loaded credentials.

Reads QWEN_API_KEY and QWEN_API_ENDPOINT from environment. The loader in
src/config/load_env.py auto-loads .env.local (or .env) if python-dotenv
is installed.

Behavior:
- Validates credentials are present
- Attempts a minimal live call if `OPENAI_BASE_URL` style endpoint is detected
  or if using default Qwen model name (mocked HTTP via OpenAI-compatible clients).
- Falls back to credential-only validation when HTTP dependencies are missing.
"""

from src.config.load_env import load_dotenv_if_present  # noqa: F401 (side effect)
from src.config import get_qwen_credentials, MissingSecretError
import os

def try_live_call(creds: dict) -> tuple[bool, str]:
    try:
        # Try OpenAI-compatible client if available
        from openai import OpenAI  # type: ignore
    except Exception:
        return False, "openai client not installed; skipping live call"

    try:
        client = OpenAI()
        # Many Qwen deployments expose an OpenAI-compatible chat/completions API.
        # We try a tiny call to validate key + routing. Providers often rely on
        # env vars like OPENAI_API_KEY/OPENAI_BASE_URL; ensure they are set if needed.
        resp = client.chat.completions.create(
            model=creds["endpoint"],
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
            temperature=0,
        )
        _ = resp.choices[0].message.content
        return True, "live call succeeded"
    except Exception as e:
        return False, f"live call failed: {e}" 


def main() -> int:
    try:
        creds = get_qwen_credentials()
    except MissingSecretError as e:
        print(f"ERROR: {e}")
        return 1

    print("Qwen credentials loaded successfully.")
    print(f"Endpoint: {creds['endpoint']}")
    print("API key: [OK]")

    # Map QWEN_* to OpenAI-compatible env vars if not set
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("QWEN_API_KEY", ""))
    # Only set OPENAI_BASE_URL if endpoint looks like a URL
    endpoint = creds["endpoint"]
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        os.environ.setdefault("OPENAI_BASE_URL", endpoint)

    ok, msg = try_live_call(creds)
    print(msg)
    return 0 if ok or "not installed" in msg else 1


if __name__ == "__main__":
    raise SystemExit(main())
