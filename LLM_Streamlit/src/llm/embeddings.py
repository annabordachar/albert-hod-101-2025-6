from openai import OpenAI
from src.config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


# Fonction qui transforme une liste de textes en embeddings vectoriels
def embed_texts(texts: list[str]) -> list[list[float]]:

    # Appel à l’API OpenAI pour générer les embeddings, chaque texte est transformé en un vecteur
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,  # Modèle d’embedding utilisé (ici 3 small )
        input=texts # Liste des textes à encoder
    )
    # Extraction des vecteurs depuis la réponse de l’API,response.data contient un embedding par texte fourni
    return [item.embedding for item in response.data]

