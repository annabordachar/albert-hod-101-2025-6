import streamlit as st

def home_button():
    # Bouton qui ramène à la page d'accueil
    if st.button("🏠 Home"):
        st.session_state.page = "Home" # Mise à jour de la page courante
        st.rerun()

def switch_page(page: str):
    # Fonction utilitaire pour changer de page
    st.session_state.page = page # Mise à jour de la page cible
    st.rerun()
