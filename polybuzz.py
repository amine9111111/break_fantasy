import streamlit as st
import requests

# Récupère la clé API (optionnelle)
API_KEY = st.secrets.get("API_KEY", None)
USE_IA = API_KEY is not None

# Configuration de la page
st.set_page_config(page_title="PolyBuzz Like IA", page_icon="🤖")
st.title("🎯 Quiz PolyBuzz Like + IA")
st.markdown("Réponds aux questions et découvre ton score. L'IA peut aussi commenter ton résultat si tu actives la clé API !")

# Questions du quiz
quiz = [
    {
        "question": "Quel est le péché capital associé à la fierté excessive ?",
        "options": ["Envie", "Orgueil", "Luxure"],
        "answer": "Orgueil"
    },
    {
        "question": "Qui est l'espada numéro 1 dans *Bleach* ?",
        "options": ["Starrk", "Barragan", "Ulquiorra"],
        "answer": "Starrk"
    },
    {
        "question": "Combien de bits dans un octet ?",
        "options": ["8", "16", "32"],
        "answer": "8"
    },
    {
        "question": "Quel langage est utilisé avec Streamlit ?",
        "options": ["Java", "Python", "JavaScript"],
        "answer": "Python"
    }
]

# Stockage des réponses
user_answers = []
score = 0

st.subheader("📝 Réponds aux questions")
for i, q in enumerate(quiz):
    st.markdown(f"**Q{i+1}. {q['question']}**")
    choix = st.radio("Ta réponse :", q["options"], key=f"q{i}")
    user_answers.append(choix)

# Bouton de validation
if st.button("✅ Valider mes réponses"):
    st.subheader("📊 Résultats")
    for i, q in enumerate(quiz):
        if user_answers[i] == q["answer"]:
            score += 1
            st.success(f"Q{i+1} ✅ Bonne réponse")
        else:
            st.error(f"Q{i+1} ❌ Mauvaise réponse (Réponse : {q['answer']})")

    st.markdown(f"### 🧮 Score final : **{score} / {len(quiz)}**")

    # 🎁 Bonus IA
    if USE_IA:
        st.subheader("🤖 Commentaire de l'IA")
        with st.spinner("L’IA réfléchit à ton score..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                messages = [
                    {"role": "system", "content": "Tu es un professeur bienveillant, drôle et un peu sarcastique. Donne ton avis sur le score d’un élève qui vient de faire un quiz."},
                    {"role": "user", "content": f"Voici le score de l'utilisateur : {score}/{len(quiz)}. Dis ce que tu en penses avec humour."}
                ]
                data = {
                    "model": "llama3-8b-8192",
                    "messages": messages,
                    "temperature": 0.9
                }
                response = requests.post(url, headers=headers, json=data)
                result = response.json()["choices"][0]["message"]["content"]
                st.markdown(result)
            except Exception as e:
                st.error(f"Erreur IA : {e}")
    else:
        st.info("🔒 Clé API non trouvée. Aucun commentaire IA généré.")

# Footer
st.markdown("---")
st.caption("🛠️ Quiz créé avec Streamlit + IA Groq (optionnelle)")

