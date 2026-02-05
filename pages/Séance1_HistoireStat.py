import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Séance 1 : Introduction & Enjeux", page_icon="📖")

st.title("📖 Séance 1 : Les méthodes quantitatives comme outil d'argumentation")

st.markdown("""
[cite_start]Cet exercice porte sur les concepts de **quantification**, d'**épistémologie** et d'**histoire des statistiques** vus lors de la première séance[cite: 12, 540, 541].
""")

# --- INITIALISATION DU SCORE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.answered = {}

# --- QUESTIONS ---
questions = [
    {
        "id": 1,
        "question": "1. Selon le cours, comment peut-on définir la statistique ?",
        "options": [
            "L'art de manipuler des chiffres pour prouver une opinion personnelle.",
            [cite_start]"La science de la collecte, de la description, de l'analyse et de l'interprétation de données[cite: 540, 734].",
            "Une branche des mathématiques uniquement dédiée au calcul de probabilités.",
            "Un outil informatique servant exclusivement à créer des graphiques."
        ],
        "answer": 1,
        "feedback": "Exact. [cite_start]La statistique englobe tout le processus, de la collecte à l'interprétation[cite: 541, 563, 734]."
    },
    {
        "id": 2,
        "question": "2. Pourquoi dit-on que la quantification est une 'construction' ?",
        "options": [
            "Parce que les chiffres sont des objets physiques que l'on assemble.",
            [cite_start]"Parce que le processus crée une réalité qui reflète la volonté du producteur du chiffre[cite: 752, 762].",
            "Parce qu'il faut construire des ordinateurs puissants pour les calculer.",
            "Parce que les statistiques ne reposent sur aucune base réelle."
        ],
        "answer": 1,
        "feedback": "Correct. [cite_start]Le chiffre ne décrit pas simplement la réalité, il participe à sa création selon les choix du statisticien[cite: 599, 752]."
    },
    {
        "id": 3,
        "question": "3. Quel était l'enjeu principal du 'Domesday Book' (1086) en Angleterre ?",
        "options": [
            "Établir un dictionnaire de la langue anglo-saxonne.",
            [cite_start]"Recenser les terres et les biens pour fixer les impôts et les ressources de l'État[cite: 343, 344].",
            "Prédire la fin du monde par des calculs astronomiques.",
            "Lister uniquement les membres de la famille royale."
        ],
        "answer": 1,
        "feedback": "Très bien. [cite_start]C'est un exemple historique du lien entre statistique, recensement et pouvoir fiscal[cite: 343, 375]."
    },
    {
        "id": 4,
        "question": "4. William Petty (1676) voulait s'exprimer en 'termes de nombre, de poids ou de mesure'. Quel était son but ?",
        "options": [
            "Rendre ses textes plus difficiles à lire pour ses opposants.",
            [cite_start]"Utiliser des arguments fondés sur la nature plutôt que sur les opinions changeantes[cite: 420, 421].",
            "Prouver que les mathématiques sont supérieures à la philosophie.",
            "Vendre ses services de comptabilité au Roi d'Angleterre."
        ],
        "answer": 1,
        "feedback": "C'est juste. [cite_start]Petty cherchait une forme d'objectivité par la mesure visible[cite: 421, 576]."
    },
    {
        "id": 5,
        "question": "5. Face à une étude statistique, quel est le double enjeu pour un étudiant en sciences sociales ?",
        "options": [
            "Apprendre les formules par cœur et savoir coder en Python.",
            "Vérifier si les calculs ont été faits sur Excel ou Google Sheets.",
            [cite_start]"Comprendre l'idée transmise et identifier les points forts/faibles de l'argumentation[cite: 164, 165, 785, 786].",
            "Savoir réciter l'histoire des statistiques depuis la Mésopotamie."
        ],
        "answer": 2,
        "feedback": "Exactement. [cite_start]La statistique est un outil d'argumentation qu'il faut savoir lire de manière critique[cite: 162, 780]."
    }
]

# --- AFFICHAGE DU QUIZ ---
form = st.form(key='quiz_form')
user_answers = {}

for q in questions:
    st.markdown(f"### {q['question']}")
    user_answers[q['id']] = st.radio(
        "Sélectionnez votre réponse :",
        q['options'],
        key=f"q_{q['id']}",
        index=None
    )
    st.write("---")

submit_button = st.form_submit_button(label='Valider mes réponses')

# --- CORRECTION ---
if submit_button:
    current_score = 0
    for q in questions:
        selected = user_answers[q['id']]
        if selected == q['options'][q['answer']]:
            st.success(f"✅ Question {q['id']} : {q['feedback']}")
            current_score += 1
        elif selected is None:
            st.warning(f"⚠️ Question {q['id']} : Aucune réponse sélectionnée.")
        else:
            st.error(f"❌ Question {q['id']} : Mauvaise réponse. La bonne était : '{q['options'][q['answer']]}'")
    
    st.metric("Votre Score Final", f"{current_score} / {len(questions)}")
    
    if current_score == len(questions):
        st.balloons()

# --- BARRE LATÉRALE ---
st.sidebar.info("""
**Rappel de cours :**
[cite_start]La statistique est intrinsèquement liée à l'exercice du pouvoir[cite: 742, 771]. [cite_start]Elle permet de transformer le complexe en chiffres pour argumenter[cite: 576, 780].
""")