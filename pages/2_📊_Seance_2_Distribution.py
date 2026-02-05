import streamlit as st
import pandas as pd
import numpy as np
import io
import random

st.set_page_config(page_title="Séance 2 : Distributions", page_icon="📊")

st.title("📊 Séance 2 : Distributions et TCD")
st.markdown("""
**Objectif :** Utiliser un Tableau Croisé Dynamique (Pivot Table) pour passer d'une liste brute à un tableau de distribution.
""")

# --- 1. GÉNÉRATION DES DONNÉES ---
if 'dist_data' not in st.session_state:
    # On utilise une variable ordinale pour que le cumulé ait du sens
    categories = ["1. Sans Bac", "2. Bac", "3. Licence", "4. Master", "5. Doctorat"]
    weights = [0.1, 0.3, 0.35, 0.2, 0.05] # Probabilités inégales
    
    n = 200 # Taille de l'échantillon
    data = random.choices(categories, weights=weights, k=n)
    
    st.session_state.dist_data = pd.DataFrame(data, columns=["Niveau_Etude"])

# --- 2. TÉLÉCHARGEMENT ---
st.subheader("1. L'Exercice")
st.info("""
1. Téléchargez le fichier ci-dessous.
2. Créez un **Tableau Croisé Dynamique** dans une nouvelle feuille (nommez-la `Resultats`).
3. Affichez pour chaque niveau d'étude :
    * Le **Nombre** de personnes (Fréquence absolue $n_i$).
    * Le **% du total** (Fréquence relative $f_i$).
4. Sauvegardez et réimportez le fichier.
""")

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    st.session_state.dist_data.to_excel(writer, index=False, sheet_name='Donnees_Brutes')

st.download_button(
    label="📥 Télécharger le jeu de données (.xlsx)",
    data=output.getvalue(),
    file_name="exercice_distribution.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- 3. CORRECTION ROBUSTE (V2) ---
st.subheader("2. Correction Automatique")
uploaded_file = st.file_uploader("Déposez votre fichier avec le TCD ici", type=['xlsx'])

if uploaded_file:
    try:
        # A. CALCUL DE LA SOLUTION (Côté Prof)
        df_ref = st.session_state.dist_data
        correction = df_ref["Niveau_Etude"].value_counts().sort_index()
        total_ref = len(df_ref)
        
        # B. LECTURE INTELLIGENTE
        xl = pd.ExcelFile(uploaded_file)
        # On cherche une feuille qui ressemble à 'Resultats'
        sheet_target = next((s for s in xl.sheet_names if "resul" in s.lower()), xl.sheet_names[-1])
        
        # On lit TOUT comme du texte au début pour éviter les erreurs de type
        df_student = pd.read_excel(uploaded_file, sheet_name=sheet_target, header=None, dtype=str)
        
        st.write(f"Analyse de la feuille : **{sheet_target}**")
        
        # C. NETTOYAGE ET CONVERSION
        # 1. On crée une version "Texte" pour trouver les labels (ex: "Licence")
        text_content = df_student.to_string().lower()
        
        # 2. On crée une version "Numérique" pour trouver les effectifs (ex: 45)
        # On force la conversion de CHAQUE cellule en nombre. Si c'est du texte, ça devient NaN.
        df_numeric = df_student.apply(pd.to_numeric, errors='coerce')
        
        # On récupère tous les nombres présents dans la feuille, sans doublons, et on enlève les NaN
        all_numbers = set(df_numeric.values.flatten())
        # On enlève les valeurs nulles (nan)
        all_numbers = {x for x in all_numbers if pd.notna(x)}

        # D. VERIFICATION
        found_all = True
        
        # On vérifie chaque catégorie
        for cat, count_attendu in correction.items():
            # Nettoyage du label (ex: "3. Licence" -> "licence")
            label_clean = cat.split(". ")[-1].lower() if ". " in cat else cat.lower()
            
            # Étape 1 : Le label est-il là ?
            if label_clean not in text_content:
                st.warning(f"⚠️ Je ne trouve pas le label **{cat}** (ou '{label_clean}'). Vérifiez l'orthographe.")
                found_all = False
            
            # Étape 2 : Le chiffre est-il là ?
            # On cherche le nombre exact (ex: 42) ou flottant (ex: 42.0)
            elif count_attendu not in all_numbers:
                st.error(f"❌ Pour **{cat}**, j'attendais l'effectif **{count_attendu}**, mais je ne le trouve nulle part dans la feuille.")
                found_all = False
            else:
                st.success(f"✅ **{cat}** : Label et Effectif ({count_attendu}) trouvés.")

        # Vérification du Total
        if total_ref in all_numbers:
            st.success(f"✅ **Total Général** ({total_ref}) trouvé.")
        else:
            st.warning(f"⚠️ Je ne trouve pas le total général ({total_ref}).")

        if found_all:
            st.balloons()
            st.success("Excellent ! Votre TCD est valide.")

    except Exception as e:
        st.error(f"Erreur technique lors de la lecture : {e}")