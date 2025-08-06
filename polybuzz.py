import streamlit as st
import requests

# Récupère ta clé API Groq ou OpenAI
API_KEY = st.secrets.get("API_KEY", None)
USE_IA = API_KEY is not None

st.set_page_config(page_title="PolyBuzz Lite", page_icon="🤖")
st.title("🎭 Chat avec Personnage IA (style PolyBuzz)")

# Création / sélection de personnage
character = st.text_input("Nom du personnage :", "Kaiza le Guerrier")
persona = st.text_area("Écris sa personnalité / bio :", "Un vétéran fier, sarcastique et loyal.")

if st.button("Créer le personnage"):
    st.success(f"Personnage **{character}** créé \n*" + persona + "*")

# Discussion
st.subheader(f"💬 Chat avec **{character}**")
user_input = st.text_input("Toi :", key="user_input")

if user_input:
    st.markdown(f"**Toi** : {user_input}")

    if USE_IA:
        with st.spinner(f"{character} réfléchit..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            messages = [
                {"role": "system", "content": f"Tu es {character}. {persona}"},
                {"role": "user", "content": user_input}
            ]
            data = {"model": "llama3‑8b‑8192", "messages": messages, "temperature": 0.9}

            try:
                resp = requests.post(url, headers=headers, json=data)
                reply = resp.json()["choices"][0]["message"]["content"]
                st.markdown(f"**{character}** : {reply}")
            except Exception as e:
                st.error("Erreur IA :" + str(e))
    else:
        st.info("🔒 Pas de clé API détectée — mode démo non interactif")
        st.markdown(f"**{character}** : (réponse de démonstration ici)")
