import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_title="S6 | Ex. 13 : Construire une base de données", page_icon="🎲", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_6.pdf"

st.title("🎲 S6 | Ex. 13 : Construire une base de données")

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Maîtriser les méthodes d'échantillonnage, la conception de questionnaires et le recodage de variables pour construire sa propre base de données.

    ### 🧠 Le sens de l'exercice
    Les données d'enquêtes sont principalement celles qu'on peut décider de construire et collecter nous-mêmes. Pour ce faire, il est vital de savoir sélectionner les individus (échantillonnage aléatoire, stratifié, systématique ou en grappes). La formulation des questions est tout aussi centrale, car elle peut introduire de multiples biais (sélection, désirabilité sociale, cadrage). Enfin, l'exploitation de traces ou de questionnaires nécessite un recodage, une étape impliquant des choix subjectifs et inévitablement une perte d'information.
    """)

if st.button("🔄 Réinitialiser la session"):
    # Clear cache variables
    for k in ['quiz_submitted']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_echantillon, tab_biais, tab_recodage = st.tabs(["📊 1. Échantillonnage", "🕵️ 2. Biais & RGPD", "⚙️ 3. Recodage"])

# --- TAB 1 : ÉCHANTILLONNAGE ---
with tab_echantillon:
    st.subheader("Les méthodes d'échantillonnage")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown(f'''
        * **Aléatoire simple :** Même probabilité d'être tiré au sort pour tous.
        * **Stratifié :** Population divisée en sous-groupes homogènes, puis tirage.
        * **Systématique :** Tirer un individu tous les *k* pas.
        * **En grappes :** Diviser en sous-groupes naturels et interroger tous les membres de quelques grappes tirées au sort.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        ''', unsafe_allow_html=True)

    st.info("Sélectionnez la méthode d'échantillonnage correspondant à chaque situation ou propriété.")
    
    with st.form("quiz_echantillon"):
        q1 = st.radio("1. Quelle méthode présente un risque de biais majeur si la liste de départ comporte une périodicité cachée ?", 
                      ["L'échantillonnage en grappes", "L'échantillonnage systématique", "L'échantillonnage stratifié"], index=None)
        q2 = st.radio("2. Au lieu de tirer des lycéens au hasard dans toute la France, on tire au sort 10 lycées et on interroge tous les élèves de ces établissements. De quelle méthode s'agit-il ?", 
                      ["L'échantillonnage en grappes", "L'échantillonnage aléatoire simple", "L'échantillonnage stratifié"], index=None)
        q3 = st.radio("3. Quelle méthode permet d'assurer une représentativité parfaite sur les variables choisies pour créer des quotas précis ?", 
                      ["L'échantillonnage aléatoire simple", "L'échantillonnage systématique", "L'échantillonnage stratifié"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "L'échantillonnage systématique":
                st.success("Q1 : Correct ! L'échantillonnage systématique est vulnérable aux motifs répétitifs dans la base de sondage.")
            else:
                st.error("Q1 : Faux. C'est l'échantillonnage systématique.")
                errors += 1
                
            if q2 == "L'échantillonnage en grappes":
                st.success("Q2 : Correct ! Il s'agit d'un tirage de grappes entières (les lycées).")
            else:
                st.error("Q2 : Faux. Il s'agit de l'échantillonnage en grappes.")
                errors += 1
                
            if q3 == "L'échantillonnage stratifié":
                st.success("Q3 : Correct ! C'est le grand avantage de diviser préalablement la population en strates.")
            else:
                st.error("Q3 : Faux. Il s'agit de l'échantillonnage stratifié.")
                errors += 1
                
            if errors == 0:
                st.balloons()

# --- TAB 2 : BIAIS & QUESTIONNAIRE ---
with tab_biais:
    st.subheader("Biais de formulation et contraintes légales")
    
    st.info("La formulation des questions et le respect de la vie privée sont fondamentaux dans la création d'un questionnaire.")
    
    with st.form("quiz_biais"):
        q1 = st.radio("1. Si seules les personnes très motivées ou très engagées prennent le temps de répondre à un questionnaire, de quel biais s'agit-il ?", 
                      ["Le biais de désirabilité sociale", "Le biais de cadrage", "L'auto-sélection (biais de sélection)"], index=None)
        q2 = st.radio("2. 'Triez-vous toujours rigoureusement vos déchets pour protéger l'environnement ?' est une question qui risque principalement de provoquer...", 
                      ["Un biais d'échantillonnage", "Un biais de désirabilité sociale", "Un biais de survie"], index=None)
        q3 = st.radio("3. Selon le RGPD, les opinions politiques, les données de santé ou l'orientation sexuelle sont considérées comme :", 
                      ["Des données administratives libres", "Des données personnelles standard", "Des données sensibles"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "L'auto-sélection (biais de sélection)":
                st.success("Q1 : Correct ! Cela fait partie des biais de sélection, liés au comportement des répondants.")
            else:
                st.error("Q1 : Faux. C'est un biais d'auto-sélection.")
                errors += 1
                
            if q2 == "Un biais de désirabilité sociale":
                st.success("Q2 : Correct ! Le répondant va avoir tendance à surestimer ses bonnes actions pour donner une image positive de lui-même.")
            else:
                st.error("Q2 : Faux. Cela engendre un biais de désirabilité sociale.")
                errors += 1
                
            if q3 == "Des données sensibles":
                st.success("Q3 : Correct ! Ce sont des données sensibles dont la collecte et le traitement sont interdits sauf exceptions strictes.")
            else:
                st.error("Q3 : Faux. Le RGPD les classe comme données sensibles.")
                errors += 1
                
            if errors == 0:
                st.balloons()

# --- TAB 3 : RECODAGE ---
with tab_recodage:
    st.subheader("Le recodage des variables")
    
    st.info("Que ce soit pour les traces ou les questionnaires, recoder est indispensable pour l'analyse statistique, mais implique des arbitrages.")
    
    with st.form("quiz_recodage"):
        q1 = st.radio("1. Passer d'une variable continue (âge exact) à une variable catégorielle (tranche d'âge) a pour principale conséquence méthodologique :", 
                      ["L'augmentation de la taille de l'échantillon", "La perte d'information", "L'élimination automatique des biais de sélection"], index=None)
        q2 = st.radio("2. Le fait de décider si les termes 'paysan', 'journalier' et 'agriculteur' vont dans la même case illustre :", 
                      ["L'échantillonnage stratifié", "La subjectivité et l'arbitraire du chercheur", "Le nettoyage automatique des traces"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "La perte d'information":
                st.success("Q1 : Correct ! Cela simplifie l'analyse, mais détruit la finesse de la donnée initiale.")
            else:
                st.error("Q1 : Faux. L'enjeu principal est la perte d'information.")
                errors += 1
                
            if q2 == "La subjectivité et l'arbitraire du chercheur":
                st.success("Q2 : Correct ! Le recodage nécessite de faire des choix forts, ce qui introduit inévitablement l'arbitraire du chercheur.")
            else:
                st.error("Q2 : Faux. Cela illustre la subjectivité des choix de recodage.")
                errors += 1
                
            if errors == 0:
                st.balloons()