import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1] # Détermine le dossier racine du projet

DATA_PATH = BASE_DIR / "data" / "pg2267-images.html"
CHROMA_DIR = BASE_DIR / "chroma_db"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in environment")
