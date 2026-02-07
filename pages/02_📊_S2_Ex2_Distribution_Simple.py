import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="Séance 2 : Distributions", page_icon="📊", layout="wide")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📊 Séance 2 : La Distribution")
st.markdown("""
**Objectif :** Comprendre le passage de l'individu au groupe. 
D'abord par un comptage **manuel** pour saisir la logique, puis par l'automatisation **Excel** (Tableau Croisé Dynamique).
""")

# --- SCÉNARIOS COMMUNS ---
# Utilisés pour les deux modes (Manuel et Excel)
SCENARIOS = {
    "education": {
        "tag": "Education",
        "titre": "Niveau d'Étude (Sociologie)",
        "col_id": "ID_Individu",
        "col_var": "Diplome",
        "categories": ["1. Sans Bac", "2. Bac", "3. Licence", "4. Master", "5. Doctorat"],
        "weights": [0.15, 0.30, 0.30, 0.20, 0.05]
    },
    "satisfaction": {
        "tag": "Satisfaction",
        "titre": "Enquête Satisfaction (Marketing)",
        "col_id": "Ref_Client",
        "col_var": "Avis_Service",
        "categories": ["1. Très Insatisfait", "2. Insatisfait", "3. Neutre", "4. Satisfait", "5. Très Satisfait"],
        "weights": [0.10, 0.15, 0.20, 0.40, 0.15]
    },
    "transport": {
        "tag": "Transport",
        "titre": "Mode de Transport (Urbanisme)",
        "col_id": "Matricule_Usager",
        "col_var": "Transport_Principal",
        "categories": ["1. Voiture", "2. Transports en commun", "3. Vélo", "4. Marche", "5. Deux-roues"],
        "weights": [0.35, 0.40, 0.10, 0.10, 0.05]
    },
    "politique": {
        "tag": "Politique",
        "titre": "Sondage Politique (Science Po)",
        "col_id": "Code_Electeur",
        "col_var": "Intention_Vote",
        "categories": ["1. Candidat A", "2. Candidat B", "3. Candidat C", "4. Abstention", "5. Blanc/Nul"],
        "weights": [0.25, 0.22, 0.18, 0.25, 0.10]
    }
}

# --- CRÉATION DES ONGLETS ---
tab_manual, tab_excel = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# ==============================================================================
# 🟢 ONGLET 1 : MODE MANUEL
# ==============================================================================
with tab_manual:
    st.subheader("1. Exercice de comptage manuel")
    
    # --- A. Sidebar Spécifique Manuel ---
    # Note : Streamlit affiche tout dans la sidebar commune, on utilise des titres pour séparer visuellement
    with st.sidebar:
        st.markdown("---")
        st.header("📝 Aide : Mode Manuel")
        st.markdown("""
        **Méthode de comptage :**
        1. Prenez une feuille de brouillon.
        2. Parcourez la liste de gauche ligne par ligne.
        3. Faites un bâton pour chaque catégorie rencontrée.
        4. Comptez le total à la fin.
        """)

    # --- B. Gestion de l'état (Manuel) ---
    if st.button("🔄 Nouveau Cas Manuel", key="btn_manual_reset"):
        # On vide uniquement les variables manuelles
        keys_to_clear = ['manual_data', 'manual_scenario', 'manual_input', 'manual_check']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # Génération des données manuelles (Petit échantillon N=25)
    if 'manual_data' not in st.session_state:
        # Choix aléatoire
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        n = 25 # Taille réduite pour l'exercice manuel
        variable_data = random.choices(scen["categories"], weights=scen["weights"], k=n)
        ids = random.sample(range(100, 999), n)
        
        # Création DataFrame
        df = pd.DataFrame({
            scen["col_id"]: ids,
            scen["col_var"]: variable_data
        })
        # On trie par ID pour mélanger les catégories (rend l'exercice pertinent)
        df = df.sort_values(by=scen["col_id"]).reset_index(drop=True)
        
        # Template de réponse vide
        df_input = pd.DataFrame({
            "Catégorie": scen["categories"],
            "Effectif (ni)": [0] * len(scen["categories"])
        })
        
        st.session_state.manual_data = df
        st.session_state.manual_scenario = scen
        st.session_state.manual_input = df_input
        st.session_state.manual_check = False

    # Récupération des variables
    df_m = st.session_state.manual_data
    scen_m = st.session_state.manual_scenario
    
    # --- C. Interface Manuel ---
    st.info(f"Voici une liste de **{len(df_m)} individus** ({scen_m['titre']}). Comptez les effectifs pour chaque catégorie et remplissez le tableau de droite.")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("**Données Brutes**")
        st.dataframe(df_m, height=500, hide_index=True)

    with col2:
        st.markdown("**Votre Distribution** (Double-cliquez pour éditer)")
        edited_df = st.data_editor(
            st.session_state.manual_input,
            column_config={
                "Catégorie": st.column_config.TextColumn(disabled=True),
                "Effectif (ni)": st.column_config.NumberColumn(
                    min_value=0, 
                    max_value=len(df_m), 
                    step=1, 
                    required=True
                )
            },
            hide_index=True,
            key="editor_manual_grid"
        )
        
        if st.button("✅ Vérifier mes calculs", key="btn_manual_check"):
            st.session_state.manual_check = True

        # --- D. Correction Manuel ---
        if st.session_state.manual_check:
            st.divider()
            st.markdown("### 🔍 Résultats")
            
            # Calcul vérité
            true_counts = df_m[scen_m["col_var"]].value_counts()
            score = 0
            
            for index, row in edited_df.iterrows():
                cat = row["Catégorie"]
                user_val = row["Effectif (ni)"]
                true_val = true_counts.get(cat, 0)
                
                if user_val == true_val:
                    st.success(f"✅ **{cat}** : {user_val} (Correct)")
                    score += 1
                else:
                    st.error(f"❌ **{cat}** : Vous avez mis **{user_val}**, la bonne réponse est **{true_val}**.")
            
            # Vérif Total
            user_total = edited_df["Effectif (ni)"].sum()
            true_total = len(df_m)
            
            if user_total != true_total:
                st.warning(f"⚠️ Votre total est de **{user_total}**, il devrait être de **{true_total}**. Vous avez oublié ou compté en double quelqu'un.")
            
            if score == len(scen_m["categories"]):
                st.balloons()
                st.success("👏 Bravo ! Vous avez compris la logique de distribution.")


# ==============================================================================
# 🔵 ONGLET 2 : MODE EXCEL
# ==============================================================================
with tab_excel:
    st.subheader("2. Automatisation avec Excel (TCD)")

    # --- A. Sidebar Spécifique Excel ---
    with st.sidebar:
        st.markdown("---")
        st.header("📊 Aide : Mode Excel")
        st.markdown(f"""
        **Besoin de revoir le cours ?**
        📄 <a href="{URL_SLIDES}" target="_blank">Ouvrir les slides (PDF)</a>
        
        **Comment faire un TCD ?**
        1. Sélectionnez tout le tableau (**Ctrl+A**).
        2. Onglet **Insertion** > **Tableau Croisé Dynamique**.
        3. Glissez la variable en **LIGNES**.
        4. Glissez la même variable en **VALEURS**.
        
        ⚠️ *Si Excel affiche une somme :*
        * Clic sur le champ dans VALEURS.
        * **Paramètres des champs de valeur**.
        * Choisir **Nombre** (ou Compte).
        """, unsafe_allow_html=True)

    # --- B. Gestion de l'état (Excel) ---
    if st.button("🔄 Nouveau Cas Excel", key="btn_excel_reset"):
        keys_to_clear = ['excel_data', 'excel_scenario']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # Génération des données Excel (Grand échantillon N=200)
    if 'excel_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        n = random.randint(180, 250)
        variable_data = random.choices(scen["categories"], weights=scen["weights"], k=n)
        ids = random.sample(range(10000, 99999), n)
        
        df = pd.DataFrame({
            scen["col_id"]: ids,
            scen["col_var"]: variable_data
        })
        
        st.session_state.excel_data = df
        st.session_state.excel_scenario = scen

    df_e = st.session_state.excel_data
    scen_e = st.session_state.excel_scenario

    # --- C. Consignes & Téléchargement ---
    st.info(f"""
    **Contexte :** Vous analysez un fichier de **{len(df_e)} lignes** sur le thème : *{scen_e['titre']}*.
    **Consigne :** Créez un TCD pour obtenir la distribution des effectifs de la variable **`{scen_e['col_var']}`**.
    """)

    # Génération du fichier Excel
    timestamp = datetime.now().strftime("%H%M%S")
    file_name_clean = f"MQ_Ex2_{scen_e['tag']}_{timestamp}.xlsx"

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_e.to_excel(writer, index=False, sheet_name='Donnees_Brutes')

    st.download_button(
        label=f"📥 Télécharger le fichier ({file_name_clean})",
        data=output.getvalue(),
        file_name=file_name_clean,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # --- D. Upload & Correction Robuste ---
    uploaded_file = st.file_uploader("Déposez votre fichier Excel avec le TCD", type=['xlsx'], key="uploader_excel")

    if uploaded_file:
        try:
            # 1. Calcul de la solution
            correction = df_e[scen_e["col_var"]].value_counts().sort_index()
            total_ref = len(df_e)
            
            # 2. Lecture du fichier étudiant (Scan de toutes les feuilles)
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            
            found_text = set()
            found_numbers = set()
            sheet_names_scanned = []

            for sheet in wb.worksheets:
                sheet_names_scanned.append(sheet.title)
                for row in sheet.iter_rows(values_only=True):
                    for cell in row:
                        if cell is not None:
                            # On stocke le texte pour vérifier les labels
                            val_str = str(cell).strip().lower()
                            found_text.add(val_str)
                            # On stocke les nombres pour vérifier les effectifs
                            try:
                                val_float = float(cell)
                                found_numbers.add(val_float)
                                found_numbers.add(int(val_float)) 
                            except ValueError:
                                pass
            
            st.write(f"🔍 Feuilles analysées : *{', '.join(sheet_names_scanned)}*")
            
            # 3. Vérification Variable (Anti-confusion)
            var_name_lower = scen_e["col_var"].lower()
            if not any(var_name_lower in txt for txt in found_text):
                st.warning(f"⚠️ Attention : Je ne trouve pas le nom de la variable **{scen_e['col_var']}** dans votre fichier.")
            
            # 4. Affichage des résultats
            st.divider()
            cols = st.columns(2)
            found_all = True
            
            for i, (cat, count_attendu) in enumerate(correction.items()):
                # Nettoyage label pour recherche souple
                label_clean = cat.lower()
                label_text_only = cat.split(". ")[-1].lower() if ". " in cat else cat.lower()
                
                with cols[i % 2]:
                    # Check Label
                    label_found = any((label_clean in txt) or (label_text_only in txt) for txt in found_text)
                    if not label_found:
                        st.warning(f"⚠️ Label introuvable : **{cat}**")
                    
                    # Check Chiffre
                    if count_attendu in found_numbers:
                        st.success(f"✅ **{cat}** : {count_attendu}")
                    else:
                        st.error(f"❌ **{cat}** : Attendu {count_attendu}, pas trouvé.")
                        found_all = False

            # Check Total
            if total_ref in found_numbers:
                st.success(f"✅ **Total Général** ({total_ref}) correct.")
            else:
                st.warning(f"⚠️ Total général ({total_ref}) introuvable.")

            if found_all:
                st.balloons()
                st.success(f"👏 Excellent ! Exercice '{scen_e['titre']}' validé.")

        except Exception as e:
            st.error(f"Erreur technique lors de la lecture : {e}")