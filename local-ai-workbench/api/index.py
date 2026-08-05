"""Vercel serverless entry point for the AI Teacher Workbench.

This lets the SAME Flask app run on Vercel's free tier so visitors can try a
live demo without downloading anything. Vercel maps requests here and runs
`app` as a WSGI callable.

On Vercel:
  - The .env values become Vercel environment variables (set them in the
    Vercel dashboard). Your OLLAMA_API_KEY lives there, never in git.
  - PROVIDER should be "cloud" (local Ollama is not reachable from a server).
  - Disk is ephemeral: uploads and generated PDFs exist only for the life of
    a single request. That is fine for a demo.

Deploy (one-time):
  1. Push this repo to GitHub.
  2. In Vercel, import the repo (Framework: Other).
  3. Add env vars: PROVIDER=cloud, OLLAMA_API_KEY=..., CLOUD_MODEL=llama3.3.
  4. Deploy. Vercel uses vercel.json -> api/index.py as the handler.
"""
from app import app as flask_app

# Vercel expects a module-level WSGI callable named `app`.
app = flask_app
