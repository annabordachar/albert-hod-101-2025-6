import streamlit as st

#  SESSION STATE INITIALISATION
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "model_name" not in st.session_state:
    st.session_state.model_name = "gpt-4o-mini"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2


from src.ui.home import render_home
from src.ui.chat import render_chat
from src.ui.model import render_model

# Configuration globale de la page Streamlit
st.set_page_config(page_title="Othello RAG", layout="wide") # page_title : titre affiché dans l’onglet du navigateur
                                                            # layout="wide" : utilise toute la largeur de l’écran

# Routeurde l'app
# On affiche une page différente selon la valeur stockée dans st.session_state.page
if st.session_state.page == "Home": # Si la page courante est "Home", on affiche la page d’accueil
    render_home()
elif st.session_state.page == "Chat": # Si la page courante est "Chat", on affiche l’interface de chat
    render_chat()
elif st.session_state.page == "Model":# Si la page courante est "Model", on affiche la page de réglage du modèle
    render_model()
