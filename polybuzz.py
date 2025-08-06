import streamlit as st
import requests

API_KEY = st.secrets.get("API_KEY", None)
USE_IA = API_KEY is not None

st.set_page_config(page_title="Test de Cancer IA", page_icon="🩺")
st.title("🧪 Test de Dépistage du Cancer (Simulation)")

st.markdown("""
> ⚠️ Ce test est purement **informatif**. Il **ne remplace pas un vrai diagnostic médical**.
""")

# Questions
st.subheader("🩻 Réponds aux questions suivantes :")

age = st.slider("Quel est ton âge ?", 10, 100, 30)
symptomes = {
    "Perte de poids inexpliquée": st.checkbox("Perte de poids inexpliquée"),
    "Fatigue chronique": st.checkbox("Fatigue chronique"),
    "Douleurs persistantes": st.checkbox("Douleurs persistantes"),
    "Saignements inhabituels": st.checkbox("Saignements inhabituels"),
    "Masse ou bosse suspecte": st.checkbox("Masse ou bosse suspecte"),
    "Tabagisme": st.checkbox("Tu fumes (ou as fumé)"),
    "Antécédents familiaux de cancer": st.checkbox("Antécédents familiaux de cancer"),
}

# Calcul du score de risque
score = 0
for k, v in symptomes.items():
    if v:
        score += 1
if age >= 60:
    score += 1

# Bouton de validation
if st.button("🧾 Obtenir les résultats"):
    st.subheader("📊 Résultat du Test")
    st.markdown(f"**Score de risque : {score}/7**")

    if score <= 2:
        st.success("Risque faible. Mais reste vigilant.")
    elif 3 <= score <= 4:
        st.warning("Risque modéré. Un bilan médical peut être utile.")
    else:
        st.error("Risque élevé. Consulte un professionnel de santé.")

    # Bonus IA (commentaire)
    if USE_IA:
        with st.spinner("L'IA réfléchit à ton score..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                messages = [
                    {"role": "system", "content": "Tu es un médecin IA qui commente un test de dépistage en langage clair."},
                    {"role": "user", "content": f"Une personne a obtenu un score de {score}/7 au test de dépistage du cancer. Donne ton avis et conseille-lui quoi faire."}
                ]
                data = {
                    "model": "llama3-8b-8192",
                    "messages": messages,
                    "temperature": 0.7
                }
                response = requests.post(url, headers=headers, json=data)
                result = response.json()["choices"][0]["message"]["content"]
                st.markdown("### 💬 Avis IA :")
                st.markdown(result)
            except Exception as e:
                st.error(f"Erreur IA : {e}")
    else:
        st.info("🔐 Clé API manquante. Aucune réponse IA générée.")
