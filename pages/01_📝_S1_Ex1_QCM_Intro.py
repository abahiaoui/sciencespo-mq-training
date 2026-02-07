import streamlit as st
import random

st.set_page_config(page_title="Séance 1 : Introduction & Enjeux", page_icon="📖")

st.title("📖 Séance 1 : Les méthodes quantitatives comme outil d'argumentation")

st.markdown("""
Révisez les concepts clés de la première séance.
**Consigne :** Répondez à toutes les questions puis cliquez sur **Valider** pour voir les corrections.
""")

# --- 1. CONFIGURATION DES LIENS ---
# Mettez ici le lien vers votre fichier PDF brut (Raw)
BASE_URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/s%C3%A9ance_1.pdf"

# --- 2. GESTION DE L'ÉTAT ---
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

if 'shuffled_questions' not in st.session_state:
    raw_questions = [
        {
            "question": "1. Comment le cours définit-il la statistique ?",
            "correct_text": "La science de la collecte, de la description, de l'analyse et de l'interprétation de données.",
            "options": [
                "L'art de manipuler des chiffres pour prouver une opinion personnelle.",
                "La science de la collecte, de la description, de l'analyse et de l'interprétation de données.",
                "Une branche des mathématiques uniquement dédiée au calcul de probabilités.",
                "Un outil informatique servant exclusivement à créer des graphiques."
            ],
            "explanation": "La statistique couvre tout le cycle de vie de la donnée, de la collecte à l'interprétation.",
            "slide_page": 64 
        },
        {
            "question": "2. Pourquoi la quantification est-elle considérée comme une 'construction' ?",
            "correct_text": "Parce que le processus crée une réalité qui reflète la volonté du producteur du chiffre.",
            "options": [
                "Parce que les chiffres sont des objets physiques que l'on assemble.",
                "Parce que le processus crée une réalité qui reflète la volonté du producteur du chiffre.",
                "Parce qu'il faut construire des ordinateurs puissants pour les calculer.",
                "Parce que les statistiques ne reposent sur aucune base réelle."
            ],
            "explanation": "Le choix de ce qu'on compte et comment on le compte crée une représentation spécifique du monde.",
            "slide_page": 66
        },
        {
            "question": "3. Selon les 'Lamentations d'Ipou-our' (Égypte, 1750 av. J.-C.), que se passe-t-il quand les registres administratifs sont détruits ?",
            "correct_text": "Le grain devient un bien commun et l'ordre social s'effondre.",
            "options": [
                "L'armée prend le contrôle immédiat des récoltes pour éviter la famine.",
                "Le grain devient un bien commun et l'ordre social s'effondre.",
                "Les scribes sont condamnés à l'exil par le Pharaon.",
                "La population cesse de payer l'impôt mais continue de respecter les propriétés."
            ],
            "explanation": "Sans registres statistiques, la gestion de la propriété et l'administration s'effondrent.",
            "slide_page": 26
        },
        {
            "question": "4. Dans la Mésopotamie antique, quel était l'usage principal des tablettes d'argile ?",
            "correct_text": "Enregistrer la distribution de rations et le paiement d'impôts.",
            "options": [
                "Écrire des textes de loi pour les tribunaux.",
                "Enregistrer la distribution de rations et le paiement d'impôts.",
                "Cartographier les territoires conquis.",
                "Lister les généalogies des familles royales."
            ],
            "explanation": "Les premières statistiques servaient à la gestion comptable et fiscale des cités.",
            "slide_page": 24
        },
        {
            "question": "5. Que décrit le document rédigé par Auguste pour Tibère à Rome ?",
            "correct_text": "Les ressources de l'État, le nombre de citoyens en armes, les flottes et les impôts.",
            "options": [
                "Un traité de paix avec les peuples alliés.",
                "Les ressources de l'État, le nombre de citoyens en armes, les flottes et les impôts.",
                "Une liste de conseils philosophiques pour gouverner.",
                "Le calendrier des fêtes religieuses de l'Empire."
            ],
            "explanation": "Ce document servait de tableau de bord pour la gestion des ressources impériales.",
            "slide_page": 25
        },
        {
            "question": "6. D'où vient étymologiquement le terme 'Statistique' (Statistik) ?",
            "correct_text": "De l'allemand, désignant la science de la description de l'État.",
            "options": [
                "Du latin 'Status', désignant simplement l'état des choses.",
                "De l'allemand, désignant la science de la description de l'État.",
                "Du grec 'Stater', une ancienne unité de mesure de poids.",
                "De l'anglais 'State-istics', l'art de gouverner."
            ],
            "explanation": "L'école allemande voyait la statistique comme l'outil de description de l'État.",
            "slide_page": 41
        },
        {
            "question": "7. Quel contexte économique du XVIe siècle a favorisé le renouveau de la pensée quantitative ?",
            "correct_text": "L'arrivée des métaux précieux du Nouveau Monde et la rivalité entre les États européens.",
            "options": [
                "La découverte de l'imprimerie qui a facilité la diffusion des livres de comptes.",
                "L'arrivée des métaux précieux du Nouveau Monde et la rivalité entre les États européens.",
                "La fin de la guerre de Cent Ans qui a permis de lever de nouvelles armées.",
                "L'invention de la comptabilité en partie double par les Italiens."
            ],
            "explanation": "Le besoin de quantifier la richesse est né de l'essor du mercantilisme.",
            "slide_page": 34
        },
        {
            "question": "8. Quelle est la nouveauté dans l'Arithmétique Politique de William Petty (1676) ?",
            "correct_text": "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
            "options": [
                "Un manuel de comptabilité pour les marchands de Londres.",
                "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
                "Une théorie mathématique sur la probabilité de gagner aux jeux de hasard.",
                "Un dictionnaire de termes économiques."
            ],
            "explanation": "Petty a introduit une méthode argumentative basée sur des preuves tangibles et mesurables.",
            "slide_page": 36
        },
        {
            "question": "9. Quelle est la différence entre l'approche allemande et l'approche anglaise au XVIIe siècle ?",
            "correct_text": "L'allemande est descriptive (Statistik) tandis que l'anglaise est probabiliste (prédiction).",
            "options": [
                "L'allemande utilise Excel et l'anglaise utilise la calculatrice.",
                "L'allemande est descriptive (Statistik) tandis que l'anglaise est probabiliste (prédiction).",
                "L'allemande est centrée sur le commerce et l'anglaise sur la démographie.",
                "L'allemande est théorique alors que l'anglaise est purement administrative."
            ],
            "explanation": "Le cours oppose la description d'État (allemande) à l'analyse probabiliste (anglaise).",
            "slide_page": 43
        },
        {
            "question": "10. À quel moment la statistique peut-elle être 'biaisée' par le statisticien ?",
            "correct_text": "À toutes les étapes : collecte, description, analyse et interprétation.",
            "options": [
                "Uniquement lors de la collecte des données sur le terrain.",
                "Seulement lors de la création des graphiques finaux.",
                "À toutes les étapes : collecte, description, analyse et interprétation.",
                "Jamais, si le statisticien utilise des formules mathématiques officielles."
            ],
            "explanation": "Le biais peut survenir dès la formulation des questions ou lors du choix des données analysées.",
            "slide_page": 59
        },
        {
            "question": "11. Quel exemple le cours utilise-t-il pour montrer qu'un chiffre peut créer deux réalités différentes ?",
            "correct_text": "Le choix entre présenter le nombre de chômeurs ou le taux de chômage.",
            "options": [
                "La comparaison entre les budgets de la France et de l'Angleterre.",
                "Le choix entre présenter le nombre de chômeurs ou le taux de chômage.",
                "L'utilisation de différentes couleurs sur une carte électorale.",
                "Le calcul de la moyenne plutôt que de la médiane pour les salaires."
            ],
            "explanation": "Deux indicateurs réels peuvent orienter l'argumentation de manière différente.",
            "slide_page": 54
        },
        {
            "question": "12. Quel est le but ultime de ce cours de méthodes quantitatives ?",
            "correct_text": "Comprendre l'idée transmise par les chiffres et identifier les points forts/faibles de l'argumentation.",
            "options": [
                "Devenir un expert en programmation informatique.",
                "Apprendre à calculer des variances complexes sans calculatrice.",
                "Comprendre l'idée transmise par les chiffres et identifier les points forts/faibles de l'argumentation.",
                "Prouver que les sciences sociales sont plus précises que les sciences dures."
            ],
            "explanation": "L'objectif est d'acquérir un esprit critique face aux arguments chiffrés.",
            "slide_page": 68
        }
    ]
    
    for q in raw_questions:
        random.shuffle(q['options'])
    
    st.session_state.shuffled_questions = raw_questions

# --- 3. AFFICHAGE DU FORMULAIRE ---
with st.form(key='quiz_form_inline'):
    user_answers = {}
    score = 0
    
    for i, q in enumerate(st.session_state.shuffled_questions):
        st.markdown(f"**{q['question']}**")
        
        user_answers[i] = st.radio(
            "Votre réponse :",
            q['options'],
            key=f"q_{i}",
            index=None,
            label_visibility="collapsed"
        )
        
        if st.session_state.quiz_submitted:
            if user_answers[i] == q['correct_text']:
                st.success(f"✅ Correct ! {q['explanation']}")
                score += 1
            else:
                slide_url = f"{BASE_URL_SLIDES}#page={q['slide_page']}"
                st.error(f"❌ Incorrect.")
                st.markdown(
                    f"**La bonne réponse était :** {q['correct_text']}\n\n"
                    f"💡 {q['explanation']}  "
                    f"👉 <a href='{slide_url}' target='_blank' style='text-decoration:none; color:#FF4B4B;'>Voir le slide page {q['slide_page']}</a>",
                    unsafe_allow_html=True
                )
        st.write("---")

    submit_button = st.form_submit_button(label="Valider mes réponses")
    
    if submit_button:
        st.session_state.quiz_submitted = True
        st.rerun()

# --- 4. RÉSULTATS ---
if st.session_state.quiz_submitted:
    st.metric("Votre Résultat Final", f"{score} / {len(st.session_state.shuffled_questions)}")
    
    if score == len(st.session_state.shuffled_questions):
        st.balloons()
    
    if st.button("🔄 Recommencer le Quiz"):
        st.session_state.quiz_submitted = False
        for q in st.session_state.shuffled_questions:
            random.shuffle(q['options'])
        st.rerun()