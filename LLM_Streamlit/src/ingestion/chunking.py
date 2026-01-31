# Fonction qui regroupe plusieurs paragraphes en chunks de taille raisonnable
def chunk_paragraphs(paragraphs: list[dict], max_chars: int = 800) -> list[dict]:

    
    chunks = []# Liste finale des chunks
    current_text = []# Liste temporaire pour stocker le texte du chunk en cours
    current_ids = []# Liste temporaire pour stocker les ids des paragraphes du chunk en cours
    current_len = 0 # Longueur totale du texte actuellement dans le chunk

    # Parcours de tous les paragraphes dans l’ordre
    for p in paragraphs:
        # Récupération du texte du paragraphe
        text = p["text"]
        length = len(text)# Calcul de la longueur du paragraphe

        # Si ajouter ce paragraphe dépasse la taille max autorisée et que le chunk courant n’est pas vide
        if current_len + length > max_chars and current_text:
            # On finalise le chunk courant et on l’ajoute à la liste
            chunks.append(
                {
                    "text": "\n\n".join(current_text),# Texte complet du chunk
                    "paragraph_ids": current_ids, # IDs des paragraphes inclus
                }
            )
            current_text, current_ids, current_len = [], [], 0 # Réinitialisation pour commencer un nouveau chunk

        current_text.append(text)# Ajout du paragraphe au chunk courant
        current_ids.append(p["id"]) # Ajout de l’id du paragraphe correspondant

        # Mise à jour de la longueur totale du chunk courant
        current_len += length

    # Après la boucle, s’il reste un chunk non ajouté On l’ajoute à la liste finale
    if current_text:
        chunks.append(
            {
                "text": "\n\n".join(current_text),
                "paragraph_ids": current_ids,
            }
        )
    return chunks
