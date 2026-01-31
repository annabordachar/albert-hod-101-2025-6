import shutil
import chromadb
from chromadb.config import Settings

from src.config import CHROMA_DIR
from src.ingestion.load_book import load_book_html
from src.ingestion.chunking import chunk_paragraphs
from src.llm.embeddings import embed_texts


# Fonction qui construit la base vectorielle
def build_vectordb(
    html_path: str,                     # Chemin vers le fichier HTML du livre
    collection_name: str = "othello",   # Nom de la collection Chroma
    reset: bool = True,                 # Indique si on repart de zéro
):
    
    # Si reset est activé et que le dossier Chroma existe déjà on supprime complètement l’ancienne base
    if reset and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)  # On s’assure que le dossier Chroma existe (création récursive si besoin)

    # Création du client Chroma en mode persistant/stocké
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Récupération ou création de la collection de vecteurs
    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Chargement du livre HTML et extraction des paragraphes
    paragraphs = load_book_html(html_path)

    # Découpage des paragraphes en chunks plus grands
    chunks = chunk_paragraphs(paragraphs)

    # Extraction du texte brut de chaque chunk
    texts = [c["text"] for c in chunks]

    # Création des métadonnées associées à chaque chunk
    # On stocke les IDs des paragraphes d’origine sous forme de string (les listes ne sont pas accepté par chroma)
    metadatas = [
        {"paragraph_ids": ",".join(c["paragraph_ids"])}
        for c in chunks
    ]

    # Génération d’un identifiant unique pour chaque chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Calcul des embeddings vectoriels pour chaque chunk de texte
    embeddings = embed_texts(texts)

    # Insertion des données dans la collection Chroma
    collection.add(
        documents=texts,        # Texte original
        metadatas=metadatas,    # Métadonnées (IDs des paragraphes)
        embeddings=embeddings,  # Vecteurs numériques
        ids=ids,                # Identifiants uniques
    )
    return collection


# Point d’entrée si le fichier est exécuté directement
if __name__ == "__main__":
    # Import du chemin du fichier HTML du livre
    from src.config import DATA_PATH

    # Construction complète de la base vectorielle
    build_vectordb(
        html_path=str(DATA_PATH),
        reset=True,
    )
    print("ChromaDB built successfully.")
