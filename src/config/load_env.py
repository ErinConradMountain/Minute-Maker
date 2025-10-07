import os
from pathlib import Path


def load_dotenv_if_present() -> None:
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return

    # Prefer .env.local, fallback to .env
    # 1) Check current working directory (useful for tests that chdir)
    cwd = Path.cwd()
    for fname in (".env.local", ".env"):
        env_path = cwd / fname
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return

    # 2) Fallback to repo root two levels up from this file
    root = Path(__file__).resolve().parents[2]
    for fname in (".env.local", ".env"):
        env_path = root / fname
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return


# Auto-load on import for developer convenience
if os.getenv("MM_DISABLE_AUTO_DOTENV") != "1":
    load_dotenv_if_present()

