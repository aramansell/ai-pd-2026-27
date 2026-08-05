"""Configuration loader for the AI Teacher Workbench.

Every setting lives in a .env file (or the environment). Nothing hard-coded.
We try to load a .env file if one exists, then let real environment variables
take priority (useful on hosted deployments like Vercel).

This file is intentionally dependency-light so the app starts fast and gives
clear, friendly error messages when something is missing.
"""
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# .env loading (tiny, no third-party dependency)
# ---------------------------------------------------------------------------
ENV_FILE = Path(__file__).resolve().parent / ".env"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Never override a real environment variable that is already set.
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(ENV_FILE)


class Config:
    """Central access to all settings. Read from env / .env."""

    # --- App basics -------------------------------------------------------
    APP_NAME = os.getenv("APP_NAME", "AI Teacher Workbench")

    # --- Model provider: 'ollama' (default) or 'cloud' ---------------------
    # 'ollama' = Ollama running on this computer (free, offline)
    # 'cloud'  = Ollama Cloud API (free tier or paid, needs OLLAMA_API_KEY)
    PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

    # --- Local Ollama ------------------------------------------------------
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    # Model to use with local Ollama, e.g. llama3.2, llama3.1, gemma2, qwen2.5
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # --- Ollama Cloud -------------------------------------------------------
    # Ollama Cloud is OpenAI-compatible: chat completions at {CLOUD_BASE}/v1/chat/completions
    CLOUD_BASE_URL = os.getenv("CLOUD_BASE_URL", "https://api.ollama.com/v1")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
    CLOUD_MODEL = os.getenv("CLOUD_MODEL", "llama3.3")

    # --- Safety limits ------------------------------------------------------
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
    MAX_STUDENT_WORK_FILES = int(os.getenv("MAX_STUDENT_WORK_FILES", "60"))
    MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "40000"))
    REQUEST_TIMEOUT_S = int(os.getenv("REQUEST_TIMEOUT_S", "600"))

    # --- Folders ------------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads")))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", str(BASE_DIR / "output")))

    # --- Hosted / Vercel flag -----------------------------------------------
    # When running on a serverless platform, disk is ephemeral. We still keep
    # the same code path; files simply persist only for the life of the request.
    IS_HOSTED = os.getenv("VERCEL", "").lower() in ("1", "true", "yes") or os.getenv("IS_HOSTED", "").lower() in ("1", "true", "yes")

    # --- Secret key (cookies/sessions) --------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-workbench")

    @property
    def effective_model(self) -> str:
        """The model name actually used for the chosen provider."""
        return self.CLOUD_MODEL if self.PROVIDER == "cloud" else self.OLLAMA_MODEL

    @property
    def api_key_present(self) -> bool:
        return bool(self.OLLAMA_API_KEY)

    def summary(self) -> dict:
        return {
            "provider": self.PROVIDER,
            "model": self.effective_model,
            "ollama_base_url": self.OLLAMA_BASE_URL,
            "cloud_base_url": self.CLOUD_BASE_URL,
            "api_key_present": self.api_key_present,
        }


config = Config()

# Ensure folders exist (skipped harmlessly when running read-only).
for _d in (Config.UPLOAD_DIR, Config.OUTPUT_DIR):
    try:
        _d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
