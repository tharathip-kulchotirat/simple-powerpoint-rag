# Simple Powerpoint Rag

> A lightweight Retrieval-Augmented Generation (RAG) chatbot, built on top of lecture slide decks. Upload a `.pptx`, ask a question, get answers grounded in your own teaching material.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)
![License](https://img.shields.io/badge/license-Apache%202.0-green)

---

## Why this project?

Dental curricula still live primarily inside PowerPoint — lecture decks passed between faculty, residents, and students. Those slides contain years of clinical reasoning, case photos, and references that rarely make it into searchable form.

`simple-powerpoint-rag` turns that passive archive into an **interactive learning assistant**:

- Ingest lecture decks as-is — no manual transcription
- Ask natural-language questions and get slide-grounded answers
- Trace every answer back to the exact slide it came from
- Run locally or in Docker; nothing leaves your machine unless you configure it to

Built by a dentist-turned-AI engineer who got tired of Ctrl+F across 40-slide decks.

---

## Features

- 📎 **PPTX ingestion** — handles large decks (up to 500 MB upload)
- ✂️ **Chunking & embedding** of slide text for semantic retrieval
- 💬 **Streamlit chat UI** — conversational interface, no setup beyond `.env`
- 📚 **Source attribution** — see which slide each answer came from
- 🐳 **Dockerized** — one command to run the whole stack
- 🧪 **Dev tooling** — `make` targets for testing, linting, formatting

---

## Architecture

```
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────────┐
│   .pptx      │ ──▶ │  Slide parser │ ──▶ │  Embedding +    │ ──▶ │  Vector    │
│   upload     │     │  (text +      │     │  chunking       │     │  store     │
└──────────────┘     │   metadata)   │     └─────────────────┘     └─────┬──────┘
                     └───────────────┘                                   │
                                                                         ▼
┌──────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────────┐
│  Streamlit   │ ◀── │   Answer +    │ ◀── │   LLM w/        │ ◀── │  Retriever │
│  chat UI     │     │   citations   │     │   prompt (RAG)  │     │  (top-k)   │
└──────────────┘     └───────────────┘     └─────────────────┘     └────────────┘
```

Prompt templates live in [`resources/prompts/`](./resources/prompts/) and can be swapped without touching application code.

---

## Tech stack

| Layer          | Tool                                                         |
| -------------- | ------------------------------------------------------------ |
| UI             | Streamlit                                                    |
| Orchestration  | LangChain             |
| LLM            | OpenAI               |
| Embeddings     | e.g. text-embedding-3-small|
| Vector store   | FAISS |
| Slide parsing  | `python-pptx`                                                |
| Packaging      | Poetry                                                       |
| Deployment     | Docker + docker-compose                                      |

---

## Getting started

### Option 1: Docker (recommended)

```bash
git clone https://github.com/tharathip-kulchotirat/simple-powerpoint-rag.git
cd simple-powerpoint-rag
cp .env.example .env   # then fill in your API key(s)
docker compose up --build
```

Open <http://localhost:8501>.

### Option 2: Local (Poetry)

Requires Python 3.10+ and [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/tharathip-kulchotirat/simple-powerpoint-rag.git
cd simple-powerpoint-rag
poetry install
cp .env.example .env   # then fill in your API key(s)
poetry run make run
```

---

## Configuration

The app reads from a `.env` file at the project root. Example:

```env
# LLM provider
OPENAI_API_KEY=sk-...

# Optional overrides
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=4
```

<!-- TODO: Replace this block with the exact variables your app actually reads. -->

---

## Usage

1. Launch the app (`make run` or `docker compose up`).
2. Upload a `.pptx` file using the sidebar uploader.
3. Wait a moment while slides are parsed, chunked, and embedded.
4. Ask questions in the chat — for example:
   - *"Summarize the indications for root canal retreatment in this deck."*
   - *"What are the differential diagnoses listed for periapical radiolucency?"*
   - *"Which slide covers implant placement protocols?"*

Each answer includes references to the source slides.

---

## Project structure

```
simple-powerpoint-rag/
├── src/
│   └── ppt_chatbot/          # Application code
│       └── main.py           # Streamlit entry point
├── resources/
│   └── prompts/              # Prompt templates (editable without code changes)
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## Development

Common tasks are wrapped in the [`Makefile`](./Makefile):

| Command        | What it does                              |
| -------------- | ----------------------------------------- |
| `make run`     | Start the Streamlit app locally           |
| `make test`    | Run the test suite with `pytest`          |
| `make lint`    | Run `flake8` + `mypy`                     |
| `make format`  | Auto-format with `black` + `isort`        |
| `make clean`   | Remove caches and temp artifacts          |

---

## License

Licensed under the [Apache License 2.0](./LICENSE).

---

## Author

**Tharathip Kulchotirat** — Dentist · Lead AI Engineer · Founder of [Cuspal Co., Ltd.](https://www.linkedin.com/in/tharathip-kulchotirat-3b83791a7/)

If you find this useful in your own teaching or learning workflow, a ⭐ on the repo is always appreciated.

---

## Citation

If you use This Dental SOAP generator in your research or any future development, please cite:

```bibtex
@software{kul_simple_powerpoint_rag_2026,
  title     = {Kulchotirat: Simple Powerpoint RAG},
  author    = {Kulchotirat T.},
  year      = {2026},
  url       = {https://github.com/tharathip-kulchotirat/simple-powerpoint-rag},
  license   = {Apache-2.0},
}
```
