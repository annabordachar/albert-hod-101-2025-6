# Fonction qui initialise l’historique de conversation dans le session_state
def init_history(session_state: dict):
    if "history" not in session_state:# Si aucune clé "history" n’existe encore dans le session_state
        session_state["history"] = [] # On crée une liste vide pour stocker les messages


# Fonction qui ajoute un message utilisateur à l’historique
def add_user_message(session_state: dict, message: str):
    session_state["history"].append(f"User: {message}") # On ajoute le message avec le label "User:"


# Fonction qui ajoute un message de l’assistant à l’historique
def add_assistant_message(session_state: dict, message: str):
    session_state["history"].append(f"Assistant: {message}") # On ajoute le message avec le label "Assistant:"


# Fonction qui récupère l’historique complet de la conversation
def get_history(session_state: dict) -> list[str]:
    return session_state.get("history", []) # On retourne la liste des messages ou une liste vide


# Fonction qui réinitialise complètement l’historique de conversation
def clear_history(session_state: dict):
    session_state["history"] = []# On vient juste remplacer l’historique existant par une liste vide
