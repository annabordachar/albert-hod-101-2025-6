import streamlit as st
from src.ui.utils import home_button

def render_home():
    home_button()  # Bouton retour à l’accueil (si on arrive d’une autre page)

    st.title("Othello RAG Chatbot")  # Titre de la page d’accueil

    # Description  de l’application sur la page de garde
    st.markdown("""
    Ask questions about **Shakespeare's Othello** using a RAG pipeline.

    **Features**
    - Semantic search over the full play
    - Grounded answers
    - Exact textual citations
    - Streaming responses
    """)

    # Deux boutons côte à côte
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💬 Go to Chat"):  # Accès direct au chat
            st.session_state.page = "Chat"
            st.rerun()

    with col2:
        if st.button("⚙️ Model settings"):  # Accès aux réglages du modèle
            st.session_state.page = "Model"
            st.rerun()

