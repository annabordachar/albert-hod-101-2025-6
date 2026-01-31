import streamlit as st
from src.ui.utils import home_button, switch_page

from src.memory.chat_history import (
    init_history,
    clear_history,
    add_user_message,
    add_assistant_message,
    get_history,
)
from src.rag.retriever import retrieve_chunks
from src.rag.qa_chain import build_prompt
from src.llm.chat_model import stream_completion

def render_chat():
    # Barre du haut avec navigation et actions
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        home_button()  # Bouton retour à l’accueil

    with col2:
        st.button("⚙️ Model settings", on_click=lambda: switch_page("Model"))  # Accès aux réglages du modèle

    with col3:
        if st.button("🔄 Reset conversation"):  # Réinitialise la conversation
            clear_history(st.session_state)
            st.rerun()


    st.title("Chat with Othello")  # Titre de la page

    init_history(st.session_state)              # Initialisation de l’historique si absent
    st.session_state.setdefault("is_streaming", False)  # Flag pour gérer l’affichage pendant le streaming

    # Affichage de l’historique du chat
    history = get_history(st.session_state)
    for i, msg in enumerate(history):
        # Évite de dupliquer le dernier message pendant le streaming
        if st.session_state["is_streaming"] and i == len(history) - 1:
            continue
        role, content = msg.split(":", 1)
        with st.chat_message(role.lower()):
            st.markdown(content)

    # Champ de saisie utilisateur
    user_input = st.chat_input("Ask a question about Othello")
    if not user_input:
        return

    # Affichage du message utilisateur
    add_user_message(st.session_state, user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # Récupération du contexte via le RAG
    chunks = retrieve_chunks(user_input, k=5)
    prompt = build_prompt(user_input, chunks, history)

    st.session_state["is_streaming"] = True  # Début du streaming

    # Réponse de l’assistant en streaming
    with st.chat_message("assistant"): # Crée une bulle de message côté assistant
        response_box = st.empty()  # Zone Streamlit vide que l’on mettra à jour en continu
        buffer = ""     # Buffer qui accumule tous les tokens reçus

        # Appel du modèle OpenAI en streaming token par token
        for token in stream_completion(
            messages=[{"role": "user", "content": prompt}],  # Prompt RAG complet
            model=st.session_state["model_name"],   # Modèle choisi dans les settings
            temperature=st.session_state["temperature"],   # Température choisie
        ):
            buffer += token   # On ajoute le token au texte déjà reçu

            # Pendant le streaming, on n’affiche QUE la réponse, on cache les sources
            visible = buffer.split("---SOURCES---")[0]
            response_box.markdown(visible)  # Mise à jour de l’affichage en temps réel

        # Une fois le streaming terminé, on sépare la réponse et les sources
        answer, *sources_part = buffer.split("---SOURCES---")
        clean = answer.strip() # Nettoyage de la réponse finale

        # Si des sources existent, on les formate proprement abec des saut de ligne titre etc 
        if sources_part:
            sources = [
                s.strip() for s in sources_part[0].split("\n") if s.strip()
            ]
            if sources:
                clean += "\n\n**Sources:**\n"
                for s in sources:
                    clean += f"> {s}\n\n"

        # Remplacement du streaming brut par la version finale propre
        response_box.markdown(clean)

    # Sauvegarde de la réponse propre dans l’historique
    add_assistant_message(st.session_state, clean)
    st.session_state["is_streaming"] = False  # Fin du streaming
