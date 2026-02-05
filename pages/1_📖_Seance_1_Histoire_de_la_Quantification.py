import streamlit as st
import random

st.set_page_config(page_title="Séance 1 : Introduction & Enjeux", page_icon="📖")

st.title("📖 Séance 1 : Les méthodes quantitatives comme outil d'argumentation")

st.markdown("""
Révisez les concepts clés de la première séance.
**Consigne :** Répondez à toutes les questions puis cliquez sur "Valider" pour voir les corrections.
""")

# --- 1. GESTION DE L'ÉTAT ---
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
            "explanation": "La statistique couvre tout le cycle de vie de la donnée, pas seulement l'analyse."
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
            "explanation": "Le choix de ce qu'on compte crée une représentation spécifique du monde."
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
            "explanation": "Sans registre (statistique), la propriété privée et l'administration de l'État disparaissent."
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
            "explanation": "L'origine de la statistique est comptable et fiscale (ex: rations d'orge)."
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
            "explanation": "C'est un ancêtre du 'Tableau de bord' de l'État pour gérer l'Empire."
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
            "explanation": "L'approche allemande (Statistik) était littéralement la science de l'État."
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
            "explanation": "L'afflux d'or et d'argent a créé un besoin de théoriser la monnaie et les prix (mercantilisme)."
        },
        {
            "question": "8. Qu'est-ce que l'Arithmétique Politique de William Petty (1676) ?",
            "correct_text": "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
            "options": [
                "Un manuel de comptabilité pour les marchands de Londres.",
                "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
                "Une théorie mathématique sur la probabilité de gagner aux jeux de hasard.",
                "Un dictionnaire de termes économiques."
            ],
            "explanation": "Petty cherchait à objectiver le discours politique par la mesure."
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
            "explanation": "L'école allemande décrivait l'État (les faits), l'école anglaise cherchait à estimer l'inconnu par le calcul."
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
            "explanation": "La subjectivité intervient dès le choix de la question posée."
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
            "explanation": "Ces deux indicateurs décrivent le même phénomène mais racontent une histoire politique différente."
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
            "explanation": "Le cours vise à former l'esprit critique face aux données."
        }
    ]
    
    # Mélange des options pour éviter la mémorisation de la position
    for q in raw_questions:
        random.shuffle(q['options'])
    
    st.session_state.shuffled_questions = raw_questions

# --- 2. AFFICHAGE DU FORMULAIRE ---
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
        
        # Affichage de la correction UNIQUEMENT si le quiz a été soumis
        if st.session_state.quiz_submitted:
            if user_answers[i] == q['correct_text']:
                st.success(f"✅ Correct ! {q['explanation']}")
                score += 1
            elif user_answers[i] is None:
                st.warning("⚠️ Vous n'avez pas répondu.")
                st.markdown(f"**La bonne réponse était :** {q['correct_text']}")
            else:
                st.error(f"❌ Incorrect. \n\n**La bonne réponse était :** {q['correct_text']}")
                st.info(f"💡 **Explication :** {q['explanation']}")
        
        st.write("---")

    submit_button = st.form_submit_button(label="Valider mes réponses")
    
    if submit_button:
        st.session_state.quiz_submitted = True
        st.rerun()

# --- 3. RÉSULTATS ---
if st.session_state.quiz_submitted:
    st.metric("Votre Résultat Final", f"{score} / {len(st.session_state.shuffled_questions)}")
    
    if score == len(st.session_state.shuffled_questions):
        st.balloons()
    
    if st.button("🔄 Recommencer le Quiz"):
        st.session_state.quiz_submitted = False
        # Remélanger les questions pour la prochaine tentative
        for q in st.session_state.shuffled_questions:
            random.shuffle(q['options'])
        st.rerun()