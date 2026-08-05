"""Model provider: talk to either local Ollama or Ollama Cloud.

Both are OpenAI-compatible HTTP APIs, so we use the same client and only
switch the base URL, the API key, and the model name.

Local Ollama:   base URL http://localhost:11434  (no API key)
Ollama Cloud:   base URL https://api.ollama.com/v1 (OpenAI-compatible, needs API key)

We use the requests library (bundled) so the whole app works on any OS with
no browser or native runtime.
"""
from __future__ import annotations

import json
import time
from typing import Optional

import requests

from config import config

# All providers speak OpenAI's /chat/completions shape.
CHAT_PATH = "/chat/completions"
MODELS_PATH = "/models"


class ProviderError(Exception):
    """Friendly, user-facing error with actionable advice."""


class LLMProvider:
    def __init__(self) -> None:
        self.provider = config.PROVIDER
        self.timeout = config.REQUEST_TIMEOUT_S

        if self.provider == "cloud":
            if not config.api_key_present:
                raise ProviderError(
                    "You chose the Ollama Cloud provider, but OLLAMA_API_KEY is empty. "
                    "Add your key to the .env file (see SETUP.md)."
                )
            self.base_url = config.CLOUD_BASE_URL.rstrip("/")
            self.api_key = config.OLLAMA_API_KEY
            self.model = config.CLOUD_MODEL
        else:
            # Local Ollama: no key, plain HTTP. Both local and cloud expose an
            # OpenAI-compatible API under /v1/, so we add that path here.
            self.base_url = config.OLLAMA_BASE_URL.rstrip("/") + "/v1"
            self.api_key = None
            self.model = config.OLLAMA_MODEL

    # -- helpers -------------------------------------------------------------
    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    # -- public API ----------------------------------------------------------
    def is_available(self) -> bool:
        """True if the chosen provider responds. Never raises."""
        try:
            r = requests.get(
                self.base_url + MODELS_PATH,
                headers=self._headers(),
                timeout=10,
            )
            return r.status_code < 500
        except Exception:
            return False

    def list_models(self) -> list:
        """Best-effort list of models the provider offers."""
        try:
            r = requests.get(
                self.base_url + MODELS_PATH,
                headers=self._headers(),
                timeout=10,
            )
            if r.status_code != 200:
                return []
            data = r.json()
            # Local Ollama returns {"models": [{name, ...}]}
            # OpenAI-compatible returns {"data": [{id, ...}]}
            items = data.get("models") or data.get("data") or []
            out = []
            for it in items:
                name = it.get("name") or it.get("id")
                if name:
                    out.append(name)
            return out
        except Exception:
            return []

    def health_detail(self) -> dict:
        """Human-readable health status for the status box on the UI."""
        detail = {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "ok": False,
            "message": "",
        }
        if self.provider == "cloud":
            if not config.api_key_present:
                detail["message"] = "No API key in .env yet."
                return detail
            if self.is_available():
                detail["ok"] = True
                detail["message"] = "Cloud API reachable and key accepted."
            else:
                detail["message"] = (
                    "Could not reach the Cloud API. Check your key and network."
                )
            return detail

        # Local Ollama
        if not self.is_available():
            detail["message"] = (
                "Ollama does not appear to be running. Start the Ollama app "
                "or run 'ollama serve'."
            )
            return detail
        installed = self.list_models()
        if self.model not in installed:
            detail["message"] = (
                f"Ollama is running, but the model '{self.model}' is not pulled. "
                f"Run: ollama pull {self.model}"
            )
            return detail
        detail["ok"] = True
        detail["message"] = (
            f"Ollama is running and model '{self.model}' is ready."
        )
        return detail

    def chat(self, messages: list[dict], temperature: float = 0.3) -> str:
        """Send a chat completion and return the text reply.

        messages is a list of {'role': 'system'|'user'|'assistant', 'content': str}.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        url = self.base_url + CHAT_PATH
        try:
            r = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
            )
        except requests.exceptions.ConnectionError:
            if self.provider == "ollama":
                raise ProviderError(
                    "Could not connect to local Ollama at "
                    f"{self.base_url}. Start the Ollama app first."
                )
            raise ProviderError(
                "Could not connect to the Ollama Cloud API. Check your internet "
                "connection and base URL."
            )
        except requests.exceptions.Timeout:
            raise ProviderError(
                "The model took too long to reply. Try a smaller model, or "
                "shorten the documents you uploaded."
            )

        if r.status_code != 200:
            body = r.text[:400]
            raise ProviderError(
                f"The model API returned HTTP {r.status_code}. {body}"
            )

        data = r.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError):
            # Ollama's native endpoint can also nest under message.
            try:
                return data["message"]["content"].strip()
            except (KeyError, TypeError):
                raise ProviderError(
                    "The model replied in an unexpected format. Check the model "
                    "name and try again."
                )
