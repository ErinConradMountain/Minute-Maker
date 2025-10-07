import os
from pathlib import Path


def _apply_env_file(env_path: Path) -> None:
    """Load environment variables from a dotenv file with safe fallbacks."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        load_dotenv = None  # type: ignore

    if load_dotenv:
        load_dotenv(dotenv_path=env_path, override=False)

    # Ensure variables are present even if python-dotenv is unavailable or skipped
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        os.environ.setdefault(key, value)


def load_dotenv_if_present() -> None:

    # Prefer .env.local, fallback to .env
    # 1) Check current working directory (useful for tests that chdir)
    cwd = Path.cwd()
    for fname in (".env.local", ".env"):
        env_path = cwd / fname
        if env_path.exists():
            _apply_env_file(env_path)
            return

    # 2) Fallback to repo root two levels up from this file
    root = Path(__file__).resolve().parents[2]
    for fname in (".env.local", ".env"):
        env_path = root / fname
        if env_path.exists():
            _apply_env_file(env_path)
            return


# Auto-load on import for developer convenience
if os.getenv("MM_DISABLE_AUTO_DOTENV") != "1":
    load_dotenv_if_present()

