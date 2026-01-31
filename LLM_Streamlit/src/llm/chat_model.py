from typing import Generator, Iterable
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Fonction qui génère une réponse en streaming
def stream_completion(
    messages: list[dict], # Liste des messages pour matcher le format attendu par OpenAI (role / content)
    model: str = "gpt-4o-mini", # choix du modèle par default 4o-mini
    temperature: float = 0.2, # Niveau de créativité du modèle par default
) -> Generator[str, None, None]:

    # Appel à l’API OpenAI en mode streaming, permet de recevoir la réponse morceau par morceau
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True,
    )

    # Parcours des événements renvoyés par le stream, Chaque événement contient une mise à jour partielle de la réponse
    for event in stream:

        delta = event.choices[0].delta
        if delta and delta.content:# Si un nouveau morceau de texte est présent      
            yield delta.content# On renvoie uniquement ce morceau (token)


# Fonction qui génère une réponse complète du modèle (sans streaming)
def complete(
    messages: list[dict], 
    model: str = "gpt-4o-mini", 
    temperature: float = 0.2,   
) -> str:
    # Appel classique à l’API OpenAI (réponse complète en une fois)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content# Retour du texte final généré par le modèle

