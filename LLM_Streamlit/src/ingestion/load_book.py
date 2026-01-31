from pathlib import Path
from bs4 import BeautifulSoup


# Marqueur indiquant le début réel du livre dans le fichier Project Gutenberg dans l'extraction html
START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"


# Fonction qui récupère le livre en HTML et extrait les paragraphes utiles
def load_book_html(path: str) -> list[dict]:
    
    html = Path(path).read_text(encoding="utf-8", errors="ignore") # Lecture du fichier HTML depuis le disque
    start = html.find(START_MARKER)# Recherche de la position du marqueur de début du livre

    # Si le marqueur n’est pas trouvé, on arrête tout avec une erreur explicite
    if start == -1:
        raise ValueError("START marker not found")

    content = html[start:]# On garde uniquement le contenu à partir du début réel du livre
    soup = BeautifulSoup(content, "html.parser")# Parsing du HTML avec BeautifulSoup
    paragraphs = []# Liste qui contiendra tous les paragraphes extraits

    # Parcours de toutes les balises <p> du document
    for p in soup.find_all("p"):
        # Extraction du texte du paragraphe
        text = p.get_text(" ", strip=True)# get_text(" ") remplace les balises internes par des espaces
        if len(text) < 10: # On ignore les paragraphes trop courts
            continue

        # Ajout du paragraphe sous forme de dictionnaire
        paragraphs.append(
            {
                # Récupération de l’attribut id du paragraphe s’il existe
                "id": p.get("id", "unknown"),
                "text": text, # Texte brut du paragraphe
            }
        )
    return paragraphs
