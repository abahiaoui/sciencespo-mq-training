import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_title="S7 | Ex. 14 : Fondements des tests statistiques", page_icon="📈", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/seance_7_8.pdf"

st.title("📈 S7 | Ex. 14 : Les fondements des tests statistiques")

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Comprendre les principes fondamentaux de l'inférence statistique avant de passer aux calculs : la fluctuation d'échantillonnage, les intervalles de confiance et la logique de la p-valeur.

    ### 🧠 Le sens de l'exercice
    Vous êtes analyste pour un média lors des élections municipales. À 18h00, sur 100 électeurs interrogés à la sortie des urnes, 54 déclarent avoir voté pour le candidat A. L'enjeu est colossal : pouvez-vous annoncer sa victoire sans risquer la crédibilité de votre rédaction ? L'avance de 4 points est-elle statistiquement significative, ou simplement due au hasard du tirage de cet échantillon ?
    """)

if st.button("🔄 Réinitialiser la session"):
    # Clear cache variables
    for k in ['quiz_submitted']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_normal, tab_ic, tab_pval = st.tabs(["📊 1. Fluctuation & Erreur-type", "🎯 2. Intervalles de confiance", "⚖️ 3. Hypothèses & P-valeur"])

# --- TAB 1 : FLUCTUATION & ERREUR-TYPE ---
with tab_normal:
    st.subheader("La loi normale et l'erreur-type")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown(f'''
        * **Fluctuation d'échantillonnage :** Même avec une égalité parfaite (50/50), les proportions mesurées varient naturellement d'un échantillon à l'autre.
        * **Loi normale :** Les estimations se concentrent symétriquement autour du vrai résultat.
        * **Erreur-type :** Mesure de la précision. Elle diminue quand la taille de l'échantillon (N) augmente.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        ''', unsafe_allow_html=True)

    st.info("Évaluez votre compréhension de la distribution des estimations et de l'erreur-type.")
    
    with st.form("quiz_normal"):
        q1 = st.radio("1. Si l'élection est une égalité parfaite (50/50) et que vous tirez 1000 échantillons aléatoires, à quoi ressemblera la distribution des estimations ?", 
                      ["À une ligne plate continue", "À une loi normale centrée autour de 50%", "À deux pics distincts à 0% et 100%"], index=None)
        q2 = st.radio("2. Que se passe-t-il concernant l'erreur-type si vos enquêteurs interrogent 10 000 électeurs au lieu de 100 ?", 
                      ["L'erreur-type augmente proportionnellement", "L'erreur-type reste exactement la même", "L'erreur-type diminue, rendant l'estimation plus précise"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "À une loi normale centrée autour de 50%":
                st.success("Q1 : Correct ! La plupart des estimations se concentrent symétriquement autour du vrai résultat (loi normale).")
            else:
                st.error("Q1 : Faux. C'est une loi normale centrée autour de 50%.")
                errors += 1
                
            if q2 == "L'erreur-type diminue, rendant l'estimation plus précise":
                st.success("Q2 : Correct ! Plus la taille de l'échantillon est grande, plus l'incertitude se réduit.")
            else:
                st.error("Q2 : Faux. L'erreur-type diminue avec la taille de l'échantillon.")
                errors += 1
                
            if errors == 0:
                st.balloons()

# --- TAB 2 : INTERVALLES DE CONFIANCE ---
with tab_ic:
    st.subheader("La marge d'erreur et la décision à 20h00")
    
    st.info("Pour annoncer un vainqueur, il faut être sûr que l'avance n'est pas comprise dans la marge d'erreur.")
    
    with st.form("quiz_ic"):
        q1 = st.radio("1. En statistiques appliquées (et dans les médias), quel est le niveau de confiance généralement adopté pour calculer un intervalle ?", 
                      ["50%", "95%", "100%"], index=None)
        q2 = st.radio("2. Si l'estimation pour le candidat A est de 54%, et que la formule (Estimation ± 1.96 * Erreur-type) vous donne un intervalle de [48.5% - 59.5%], que décidez-vous ?", 
                      ["On annonce la victoire du candidat A", "On annonce la victoire du candidat B", "L'élection est trop serrée pour annoncer un vainqueur (Too close to call)"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "95%":
                st.success("Q1 : Correct ! On fixe généralement un niveau de sécurité de 95%.")
            else:
                st.error("Q1 : Faux. Le niveau standard est de 95%.")
                errors += 1
                
            if q2 == "L'élection est trop serrée pour annoncer un vainqueur (Too close to call)":
                st.success("Q2 : Correct ! Le seuil des 50% se trouve à l'intérieur de l'intervalle de confiance, on ne peut donc rien annoncer de manière catégorique.")
            else:
                st.error("Q2 : Faux. Puisque 50% est dans l'intervalle, c'est trop serré pour se prononcer.")
                errors += 1
                
            if errors == 0:
                st.balloons()

# --- TAB 3 : HYPOTHÈSES & P-VALEUR ---
with tab_pval:
    st.subheader("Les 7 étapes et la règle de décision")
    
    st.info("Le test d'hypothèse consiste à tenter de rejeter mathématiquement l'hypothèse que les résultats sont dus au hasard.")
    
    with st.form("quiz_pval"):
        q1 = st.radio("1. Dans notre élection municipale, que représente l'hypothèse nulle (H0) ?", 
                      ["Le candidat A a réellement gagné", "L'élection est une égalité parfaite (score réel = 50%), l'écart n'est dû qu'au hasard", "L'échantillon est biaisé"], index=None)
        q2 = st.radio("2. Quelle est la définition correcte de la p-valeur ?", 
                      ["La probabilité que notre hypothèse alternative (H1) soit fausse", "La probabilité d'obtenir ces résultats uniquement grâce au hasard, si l'hypothèse nulle (H0) était vraie", "La probabilité exacte que le candidat A gagne l'élection"], index=None)
        q3 = st.radio("3. Si la p-valeur de notre test de Student est de 0,02 (2%), quelle est la conclusion finale ?", 
                      ["On rejette H0, le résultat est statistiquement significatif", "On ne rejette pas H0, le hasard reste une explication trop probable", "Le test est non concluant"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "L'élection est une égalité parfaite (score réel = 50%), l'écart n'est dû qu'au hasard":
                st.success("Q1 : Correct ! L'hypothèse nulle (H0) représente toujours le hasard ou l'égalité parfaite.")
            else:
                st.error("Q1 : Faux. L'hypothèse nulle stipule que le score est de 50%.")
                errors += 1
                
            if q2 == "La probabilité d'obtenir ces résultats uniquement grâce au hasard, si l'hypothèse nulle (H0) était vraie":
                st.success("Q2 : Correct ! C'est la règle d'or pour bien interpréter une p-valeur.")
            else:
                st.error("Q2 : Faux. C'est la probabilité d'observer ces données si H0 est vraie.")
                errors += 1
                
            if q3 == "On rejette H0, le résultat est statistiquement significatif":
                st.success("Q3 : Correct ! Puisque p < 0,05, la probabilité que l'écart soit dû au hasard est très faible. On peut annoncer le vainqueur.")
            else:
                st.error("Q3 : Faux. Une p-valeur inférieure à 0,05 implique le rejet de H0.")
                errors += 1
                
            if errors == 0:
                st.balloons()