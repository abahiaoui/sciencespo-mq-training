import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="Séance 2 : Distributions", page_icon="📊")

st.title("📊 Séance 2 : Distributions et TCD")
st.markdown("""
**Objectif :** Utiliser un Tableau Croisé Dynamique (Pivot Table) pour transformer une liste d'individus en tableau de distribution.
""")

# --- 1. GÉNÉRATION DES DONNÉES ---
if 'dist_data' not in st.session_state:
    n = 200
    categories = ["1. Sans Bac", "2. Bac", "3. Licence", "4. Master", "5. Doctorat"]
    weights = [0.15, 0.30, 0.30, 0.20, 0.05]
    education = random.choices(categories, weights=weights, k=n)
    ids = random.sample(range(10000, 99999), n)
    
    st.session_state.dist_data = pd.DataFrame({
        "ID_Individu": ids,
        "Niveau_Etude": education
    })

# --- 2. TÉLÉCHARGEMENT ---
st.subheader("1. L'Exercice")
st.info("""
**Contexte :** Vous analysez les résultats d'une enquête sociologique sur 200 individus.
**Consignes :**
1. Téléchargez le fichier.
2. Créez un **Tableau Croisé Dynamique** (peu importe le nom de la feuille).
3. Calculez pour la variable `Niveau_Etude` :
    * Le **Nombre** d'individus.
    * Le **% du total**.
""")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name_unique = f"exercice_distribution_{timestamp}.xlsx"

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    st.session_state.dist_data.to_excel(writer, index=False, sheet_name='Donnees_Brutes')

st.download_button(
    label=f"📥 Télécharger le jeu de données",
    data=output.getvalue(),
    file_name=file_name_unique,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- 3. CORRECTION SCAN TOTAL ---
st.subheader("2. Correction Automatique")
uploaded_file = st.file_uploader("Déposez votre fichier (.xlsx) ici", type=['xlsx'])

if uploaded_file:
    try:
        # A. CALCUL DE LA SOLUTION
        df_ref = st.session_state.dist_data
        correction = df_ref["Niveau_Etude"].value_counts().sort_index()
        total_ref = len(df_ref)
        
        # B. LECTURE DE TOUT LE CLASSEUR
        # data_only=True récupère les valeurs calculées des TCD
        wb = openpyxl.load_workbook(uploaded_file, data_only=True)
        
        # Ensembles globaux pour stocker TOUT ce qui est écrit dans le fichier
        found_text = set()
        found_numbers = set()
        
        # On parcourt TOUTES les feuilles du fichier
        sheet_names_scanned = []
        for sheet in wb.worksheets:
            sheet_names_scanned.append(sheet.title)
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if cell is not None:
                        # Stockage Texte (minuscule)
                        val_str = str(cell).strip().lower()
                        found_text.add(val_str)
                        
                        # Stockage Nombre (Entier et Float)
                        try:
                            val_float = float(cell)
                            found_numbers.add(val_float)
                            found_numbers.add(int(val_float)) 
                        except ValueError:
                            pass
        
        st.write(f"Feuilles analysées : *{', '.join(sheet_names_scanned)}*")
        
        # D. VÉRIFICATION
        found_all = True
        st.divider()
        
        # On vérifie chaque catégorie
        for cat, count_attendu in correction.items():
            # Nettoyage du label (ex: "3. Licence" -> "licence")
            label_clean = cat.split(". ")[-1].lower() if ". " in cat else cat.lower()
            
            col1, col2 = st.columns([3, 1])
            
            # Recherche souple du texte
            # On cherche si "licence" apparait dans un des textes trouvés
            label_found = any(label_clean in txt for txt in found_text)
            
            if not label_found:
                col1.warning(f"⚠️ Label introuvable : **{cat}**")
                # On ne bloque pas found_all pour le texte, car Excel renome parfois les lignes
            
            if count_attendu not in found_numbers:
                col1.error(f"❌ **{cat}** : Je ne trouve pas l'effectif **{count_attendu}** dans le fichier.")
                found_all = False
            else:
                col1.success(f"✅ **{cat}** : {count_attendu} répondants trouvés.")

        # Vérification du Total
        if total_ref in found_numbers:
            st.success(f"✅ **Total Général** ({total_ref}) correct.")
        else:
            st.warning(f"⚠️ Je ne trouve pas le total général ({total_ref}). Avez-vous pensé aux totaux ?")

        if found_all:
            st.balloons()
            st.success("👏 Bravo ! Votre Tableau Croisé Dynamique est correct.")

    except Exception as e:
        st.error(f"Erreur technique : {e}")