# TUN AI

Professional, responsive AI encyclopedia starter website with Arabic, French and English UI.

## Included
- Responsive dark/light interface
- AI chat backend using an open model through Hugging Face Inference Providers
- Wikipedia search in English, French and Arabic
- Server-side secret handling (the AI token is never placed in browser JavaScript)
- Render deployment blueprint and Dockerfile

## Run locally
1. Install Python 3.10+
2. In this folder, create and activate a virtual environment:
   `python -m venv .venv`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set your Hugging Face token.
5. Run:
   `uvicorn app:app --reload`
6. Open `http://127.0.0.1:8000`

## Configure AI
Create a Hugging Face access token at `https://huggingface.co/settings/tokens`.
Set it as `HF_TOKEN` in your local `.env`, or as a secret environment variable in your hosting dashboard.
Default model: `Qwen/Qwen2.5-7B-Instruct`. Inference availability, provider support, and free quotas can change; select a model/provider available to your account if this one is unavailable.

**Never send your token in chat, put it in `static/` files, or commit `.env` to GitHub.**

## Publish online with Render
1. Create a GitHub account and a new repository.
2. Upload the contents of this folder to the repository (do not upload `.env`).
3. Create/sign in to Render and choose **New → Blueprint**; connect the repository containing `render.yaml`.
4. Render reads `render.yaml`. During setup, enter your Hugging Face token as the `HF_TOKEN` secret environment variable.
5. Deploy. When the deployment succeeds, Render gives you a public `*.onrender.com` address.

The free web service may sleep when idle and wake more slowly. Hosting and AI inference quotas/availability are controlled by those providers. A custom domain is optional.

## Status
This package is deployment-ready, but it is **not yet a live public website**. Publishing requires the owner to connect a GitHub repository, create the hosting service, and enter their private AI token in the hosting dashboard. I cannot create accounts or accept private credentials on the owner's behalf.
