import streamlit as st
from src.ui.utils import home_button, switch_page

def render_model():
    # Barre du haut avec navigation
    col1, col2 = st.columns([1, 6])

    with col1:
        home_button()  # Bouton retour à la page Home

    with col2:
        st.button("💬 Go to Chat", on_click=lambda: switch_page("Chat"))  # Accès direct au chat

    st.title("Model settings")  # Titre de la page

    # Sélection du modèle (valeur locale, modifiable)
    model = st.selectbox(
        "Model",  # Label affiché
        options=[
            "gpt-4o-mini",
            "gpt-4.1-mini",
            "gpt-3.5-turbo",
        ],
        # Index calculé à partir du modèle actuellement stocké en session
        index=[
            "gpt-4o-mini",
            "gpt-4.1-mini",
            "gpt-3.5-turbo",
        ].index(st.session_state.get("model_name", "gpt-4o-mini")),
    )

    # Slider de température (valeur locale, modifiable)
    temperature = st.slider(
        "Temperature",  # Label
        min_value=0.0, # Valeur minimale
        max_value=1.0,  # Valeur maximale
        step=0.1, # Pas
        value=st.session_state.get("temperature", 0.2),  # Valeur actuelle
    )

    # Bouton de sauvegarde explicite
    if st.button("💾 Save settings"):
        # Sauvegarde des paramètres dans la session
        st.session_state.model_name = model
        st.session_state.temperature = temperature

        st.success("Settings saved.")  # Message de confirmation
        st.rerun()  # Recharge l’app pour appliquer les changements partout
