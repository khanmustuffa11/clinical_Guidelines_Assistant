# clinical_Guidelines_Assistant

A retrieval-augmented generation system that answers clinical questions
using official medical guidelines.

⚠️ This tool is for educational purposes only.

## Features
- Grounded clinical answers
- Source-aware retrieval
- FastAPI backend
- Streamlit frontend

## Setup
1. Create virtual environment
2. Install requirements
3. Add API keys
4. Run ingestion
5. Start API & frontend
clinical-guidelines-rag/
│
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── data/
│   └── guidelines/
│       ├── diabetes/
│       │   └── example_diabetes_guideline.pdf
│       ├── hypertension/
│       │   └── example_hypertension_guideline.pdf
│
├── vectordb/
│   └── chroma/              # auto-created at runtime
│
├── app/
│   ├── __init__.py
│
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pdf_loader.py
│   │   ├── chunking.py
│   │   └── ingest.py
│
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   └── generator.py
│
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│
│   └── frontend/
│       └── streamlit_app.py
│
├── scripts/
│   └── run_ingestion.sh
│
└── tests/
    └── test_smoke.py
