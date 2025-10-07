"""
Configuration settings for Whisper transcription.
"""

import os
from typing import Dict, Any, Optional


def get_default_whisper_config() -> Dict[str, Any]:
    """Get default Whisper configuration."""
    return {
        # Provider selection: local | openai | whisper_api
        "provider": os.getenv("WHISPER_PROVIDER", None),  # if None, derived from use_openai_api
        "model_name": os.getenv("WHISPER_MODEL", "base"),
        "use_openai_api": os.getenv("USE_OPENAI_WHISPER_API", "false").lower() == "true",
        "language": os.getenv("WHISPER_LANGUAGE"),  # Auto-detect if None
        "prompt": os.getenv("WHISPER_PROMPT"),  # No prompt if None
        "temperature": float(os.getenv("WHISPER_TEMPERATURE", "0")),
        "best_of": int(os.getenv("WHISPER_BEST_OF", "5")),
        "beam_size": int(os.getenv("WHISPER_BEAM_SIZE", "5")),
        # Third-party Whisper API configuration
        "api_base_url": os.getenv("WHISPER_API_BASE_URL"),
        "api_key": os.getenv("WHISPER_API_KEY"),
        "api_endpoint": os.getenv("WHISPER_API_ENDPOINT", "/v1/transcriptions"),
    }


def validate_whisper_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize Whisper configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Validated configuration
    """
    validated = get_default_whisper_config()
    validated.update(config)
    
    # Determine provider with backward compatibility for use_openai_api
    if validated.get("provider"):
        provider = validated["provider"].strip().lower()
    else:
        provider = "openai" if validated.get("use_openai_api") else "local"
    validated["provider"] = provider

    # Validate model name
    valid_models = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
    if provider == "local" and validated["model_name"] not in valid_models:
        validated["model_name"] = "base"
    
    # Validate temperature
    if not 0 <= validated["temperature"] <= 1:
        validated["temperature"] = 0
    
    # Validate best_of and beam_size
    if validated["best_of"] < 1:
        validated["best_of"] = 5
    if validated["beam_size"] < 1:
        validated["beam_size"] = 5

    # Validate third-party API settings if selected
    if provider == "whisper_api":
        # Require base URL and API key for third-party provider
        if not validated.get("api_base_url"):
            validated["api_base_url"] = "https://api.whisper-api.com"
        # api_key intentionally not defaulted for security; must be provided via env
    
    return validated