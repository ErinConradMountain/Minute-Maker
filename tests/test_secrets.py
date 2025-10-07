import os
import pytest
import importlib


def test_get_qwen_credentials_raises_when_missing(monkeypatch):
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    with pytest.raises(Exception):
        import src.config.secrets as secrets
        secrets.get_qwen_credentials()


def test_load_env_auto_loads_tmp(tmp_path, monkeypatch):
    # Create a temp project with .env.local and ensure loader finds it
    env_file = tmp_path / ".env.local"
    env_file.write_text("QWEN_API_KEY=abc123\n")

    # Point the loader to tmp_path by temporarily adjusting module path logic.
    import src.config.load_env as load_env
    # Monkeypatch the module's computed root to tmp_path
    monkeypatch.setenv("MM_DISABLE_AUTO_DOTENV", "0")
    # Replace Path.resolve used inside load_env to return a fake path under tmp_path
    import pathlib

    original_resolve = pathlib.Path.resolve

    def fake_resolve(self):
        # Pretend load_env.py lives at tmp_path/src/config/load_env.py
        fake_file = tmp_path / "src" / "config" / "load_env.py"
        return pathlib.Path(fake_file)

    monkeypatch.setattr(pathlib.Path, "resolve", fake_resolve, raising=False)
    try:
        importlib.reload(load_env)
    finally:
        monkeypatch.setattr(pathlib.Path, "resolve", original_resolve, raising=False)

    assert os.getenv("QWEN_API_KEY") == "abc123"
