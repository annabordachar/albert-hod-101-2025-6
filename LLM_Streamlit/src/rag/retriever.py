import chromadb
from src.config import CHROMA_DIR
from src.llm.embeddings import embed_texts

# Fonction qui charge une collection Chroma persistante existante
def get_retriever(collection_name: str = "othello"):
    # Création d’un client Chroma en mode persistant, on pointe vers le dossier CHROMA_DIR où la base vectorielle est stockée sur disque
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )
    return client.get_collection(name=collection_name) # Récupération de la collection demandée (ici: "othello"), cette collection contient tous les chunks vectorisés



# Fonction principale de récupération des chunks pertinents
def retrieve_chunks(
    question: str,   # Question posée par l’utilisateur
    k: int = 5,      # Nombre de chunks les plus pertinents à récupérer
):
   
    collection = get_retriever() # Chargement de la collection Chroma
    query_embedding = embed_texts([question])[0] # Calcul de l’embedding de la question utilisateur embed_texts renvoie une liste de vecteurs, on prend le premier

    # Recherche des chunks similaire dans la collection Chroma qui compare l’embedding de la question avec ceux des chunks
    results = collection.query(
        query_embeddings=[query_embedding],  # vecteur de la question
        n_results=k, # nombre de résultats souhaités
        include=["documents", "metadatas"],  # on récupère le texte + les métadonnées
    )

    chunks = []
    for doc, meta, cid in zip( # Boucle sur les résultats retournés par Chroma
        results["documents"][0], #textes des chunks
        results["metadatas"][0],
        results["ids"][0], # identifiants uniques des chunks
    ):
        # organisation de l'output en dictionnaire remplie à chaque boucle
        chunks.append(
            {
                "chunk_id": cid,   
                "text": doc,       
                "paragraph_ids": meta["paragraph_ids"].split(","), # Les IDs de paragraphes sont stockés sous forme de string ( à cause de chrOma) on les reconvertit en liste avec split(",")

            }
        )
    return chunks
