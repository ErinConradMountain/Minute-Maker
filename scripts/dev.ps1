param(
  [ValidateSet('init','test','qwen','whisper','all')]
  [string]$Task = 'init',
  [string]$Audio = 'assets/sample.wav'
)

$ErrorActionPreference = 'Stop'

function Ensure-Venv {
  if (-not (Test-Path .venv)) {
    Write-Host 'Creating virtual environment (.venv)...'
    python -m venv .venv
  }
  Write-Host 'Activating virtual environment...'
  . .\.venv\Scripts\Activate.ps1
}

function Install-DevDeps {
  Write-Host 'Upgrading pip and installing dev dependencies...'
  python -m pip install --upgrade pip
  python -m pip install -r requirements-dev.txt
}

function Ensure-OpenAI {
  try {
    python -c "import openai" 2>$null | Out-Null
  } catch {
    Write-Host 'Installing openai client...'
    python -m pip install openai
  }
}

function Set-PyPath {
  $env:PYTHONPATH = "$pwd"
}

switch ($Task) {
  'init' {
    Ensure-Venv
    Install-DevDeps
    Set-PyPath
    Write-Host 'Done. You can now run: pytest -q'
  }
  'test' {
    Ensure-Venv
    Install-DevDeps
    Set-PyPath
    python -m pytest -q
  }
  'qwen' {
    Ensure-Venv
    Install-DevDeps
    Ensure-OpenAI
    Set-PyPath
    python scripts/check_qwen.py
  }
  'whisper' {
    Ensure-Venv
    Install-DevDeps
    Ensure-OpenAI
    Set-PyPath
    if (-not (Test-Path $Audio)) {
      Write-Host "Generating sample audio at $Audio ..."
      python scripts/gen_sample_audio.py $Audio
    }
    python scripts/check_whisper.py $Audio
  }
  'all' {
    Ensure-Venv
    Install-DevDeps
    Ensure-OpenAI
    Set-PyPath
    python -m pytest -q
    if (-not (Test-Path $Audio)) { python scripts/gen_sample_audio.py $Audio }
    python scripts/check_qwen.py
    python scripts/check_whisper.py $Audio
  }
}

