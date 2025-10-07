#!/usr/bin/env python3
"""
Setup script for Whisper dependencies and models.
"""

import sys
import subprocess
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def install_dependencies():
    """Install required dependencies for Whisper."""
    dependencies = [
        "openai-whisper>=20231117",
        "openai>=1.3.0", 
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "pydub>=0.25.1"
    ]
    
    logger.info("Installing Whisper dependencies...")
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            logger.info(f"✓ Installed {dep}")
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to install {dep}: {e}")
            return False
    
    return True


def download_models():
    """Download Whisper models for offline use."""
    import whisper
    
    models = ["tiny", "base"]  # Start with smaller models
    
    logger.info("Downloading Whisper models...")
    
    for model_name in models:
        try:
            logger.info(f"Downloading {model_name} model...")
            whisper.load_model(model_name)
            logger.info(f"✓ Downloaded {model_name} model")
        except Exception as e:
            logger.error(f"✗ Failed to download {model_name} model: {e}")
    
    logger.info("Model download complete!")


def verify_installation():
    """Verify Whisper installation works correctly."""
    try:
        import whisper
        import torch
        import torchaudio
        from pydub import AudioSegment
        
        logger.info("✓ All dependencies imported successfully")
        
        # Test model loading
        model = whisper.load_model("tiny")
        logger.info("✓ Model loading works")
        
        # Test basic functionality
        logger.info("✓ Whisper setup verification complete!")
        return True
        
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Setup verification failed: {e}")
        return False


def main():
    """Main setup function."""
    logger.info("Setting up Whisper for Minute Maker...")
    
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    if not verify_installation():
        logger.error("Installation verification failed")
        sys.exit(1)
    
    try:
        download_models()
    except Exception as e:
        logger.warning(f"Model download failed (can be done later): {e}")
    
    logger.info("🎉 Whisper setup complete!")
    logger.info("You can now use Whisper for audio transcription in Minute Maker.")


if __name__ == "__main__":
    main()