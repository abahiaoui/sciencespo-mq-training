import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="Séance 2 : Groupement", page_icon="📈", layout="wide")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📈 Séance 2 : Le Groupement par Intervalles")
st.markdown("""
**Objectif :** Transformer une variable quantitative **continue** (ex: salaire, note, âge) en **classes** (tranches).
Commencez par le mode manuel pour comprendre la logique, puis passez à Excel.
""")

# --- SCÉNARIOS ---
SCENARIOS = {
    "notes": {
        "tag": "Notes", "titre": "Les Mentions (Éducation)", "unit": "/20",
        "min": 10, "max": 20, "mean": 14.5, "std": 2.5, "digits": 2,
        "step": 2,
        "bins": [10, 12, 14, 16, 18, 20.1],
        "labels": ["10 à <12", "12 à <14", "14 à <16", "16 à <18", "18 à 20"]
    },
    "revenus": {
        "tag": "Revenus", "titre": "Salaires (Économie)", "unit": "€",
        "min": 1500, "max": 4000, "mean": 2600, "std": 600, "digits": 0,
        "step": 500,
        "bins": [1500, 2000, 2500, 3000, 3500, 4001],
        "labels": ["1500 à <2000", "2000 à <2500", "2500 à <3000", "3000 à <3500", "3500 à 4000"]
    },
    "age": {
        "tag": "Age", "titre": "Pyramide des Âges (Démographie)", "unit": "ans",
        "min": 20, "max": 70, "mean": 45, "std": 15, "digits": 0,
        "step": 10,
        "bins": [20, 30, 40, 50, 60, 70.1],
        "labels": ["20 à <30", "30 à <40", "40 à <50", "50 à <60", "60 à 70"]
    }
}

# --- CRÉATION DES ONGLETS ---
tab_manual, tab_excel = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# ==============================================================================
# 🟢 ONGLET 1 : MODE MANUEL
# ==============================================================================
with tab_manual:
    st.subheader("1. Création de classes à la main")
    
    # --- Sidebar Spécifique ---
    with st.sidebar:
        st.header("📝 Aide : Mode Manuel")
        st.markdown(f"""
        **Ressource :**
        📄 <a href="{URL_SLIDES}" target="_blank">Slides du cours</a>
        
        ---
        **Règle des intervalles [a, b[ :**
        * **Borne de début (a)** : Incluse (on compte).
        * **Borne de fin (b)** : Exclue (on ne compte pas, ça va dans la suivante).
        
        *Exemple :*
        Dans l'intervalle **10 à <12** :
        * 10 est compté.
        * 11.9 est compté.
        * 12 va dans l'intervalle suivant.
        """, unsafe_allow_html=True)

    # --- Gestion État ---
    if st.button("🔄 Nouveau Cas Manuel", key="btn_grp_man"):
        keys_to_del = ['grp_man_data', 'grp_man_scen', 'grp_man_input', 'grp_man_check']
        for k in keys_to_del:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    if 'grp_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        n = 20 # Petit échantillon
        # Uniforme pour avoir des données un peu partout
        raw = np.random.uniform(scen["min"], scen["max"], n)
        clean = np.round(raw, scen["digits"])
        clean.sort() # TRIÉ pour faciliter le travail manuel
        
        df = pd.DataFrame(clean, columns=["Valeur"])
        df_input = pd.DataFrame({"Intervalle": scen["labels"], "Effectif": [0]*len(scen["labels"])})
        
        st.session_state.grp_man_data = df
        st.session_state.grp_man_scen = scen
        st.session_state.grp_man_input = df_input
        st.session_state.grp_man_check = False

    df_m = st.session_state.grp_man_data
    scen_m = st.session_state.grp_man_scen

    # --- Interface ---
    st.info(f"Voici **20 valeurs triées** ({scen_m['titre']}). Classez-les par intervalles de **{scen_m['step']} {scen_m['unit']}** dans le tableau de droite.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Données Triées**")
        st.dataframe(df_m, height=600, hide_index=True)
    
    with col2:
        st.markdown("**Votre Groupement**")
        edited_df = st.data_editor(
            st.session_state.grp_man_input,
            column_config={
                "Intervalle": st.column_config.TextColumn(disabled=True),
                "Effectif": st.column_config.NumberColumn(min_value=0, max_value=20, step=1)
            },
            hide_index=True,
            key="editor_grp_man"
        )
        
        if st.button("✅ Vérifier mes calculs", key="check_grp_man"):
            st.session_state.grp_man_check = True
            
        # --- Correction ---
        if st.session_state.grp_man_check:
            st.divider()
            # pd.cut fait le calcul théorique
            sol = pd.cut(df_m["Valeur"], bins=scen_m["bins"], labels=scen_m["labels"], right=False)
            true_counts = sol.value_counts().sort_index()
            
            score = 0
            for idx, row in edited_df.iterrows():
                lbl = row["Intervalle"]
                val = row["Effectif"]
                true_val = true_counts.get(lbl, 0)
                
                if val == true_val:
                    st.success(f"✅ {lbl} : {val}")
                    score += 1
                else:
                    st.error(f"❌ {lbl} : Vous avez mis **{val}**, la réponse est **{true_val}**.")
            
            # Check Total
            user_total = edited_df["Effectif"].sum()
            if user_total != 20:
                st.warning(f"⚠️ Total incorrect : {user_total} (Attendu : 20).")
            
            if score == len(scen_m["labels"]):
                st.balloons()
                st.success("👏 Bravo ! La logique est acquise.")


# ==============================================================================
# 🔵 ONGLET 2 : MODE EXCEL
# ==============================================================================
with tab_excel:
    st.subheader("2. Groupement automatique avec Excel")

    # --- Sidebar Spécifique ---
    with st.sidebar:
        st.markdown("---")
        st.header("📊 Aide : Mode Excel")
        
        if 'grp_xl_scen' in st.session_state:
            curr_step = st.session_state.grp_xl_scen['step']
            curr_min = st.session_state.grp_xl_scen['min']
            curr_max = st.session_state.grp_xl_scen['max']
        else:
            curr_step = "X"
            curr_min = "Min"
            curr_max = "Max"

        st.markdown(f"""
        **Procédure de Groupement :**
        1. Faites votre TCD (Variable en Lignes, ID en Valeurs).
        2. **Clic Droit** sur une valeur de la première colonne (gauche).
        3. Cliquez sur **Grouper...**
        4. Configurez :
            * **Début :** {curr_min}
            * **Fin :** {curr_max}
            * **Par :** {curr_step}
        """)

    # --- Gestion État ---
    if st.button("🔄 Nouveau Cas Excel", key="btn_grp_xl"):
        if 'grp_xl_data' in st.session_state: del st.session_state['grp_xl_data']
        st.rerun()

    if 'grp_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 300 # Grand échantillon
        # Distribution Normale pour plus de réalisme
        raw = np.random.normal(scen["mean"], scen["std"], n)
        clean = np.clip(raw, scen["min"], scen["max"])
        clean = np.round(clean, scen["digits"])
        
        ids = random.sample(range(10000, 99999), n)
        df = pd.DataFrame({"ID": ids, "Variable": clean})
        
        st.session_state.grp_xl_data = df
        st.session_state.grp_xl_scen = scen

    df_e = st.session_state.grp_xl_data
    scen_e = st.session_state.grp_xl_scen

    # --- Interface ---
    st.info(f"""
    **Contexte :** Fichier de **{len(df_e)} lignes**. Variable : `{scen_e['titre']}`.
    **Consigne :** Créez un TCD et **Groupez** la variable par pas de **{scen_e['step']}**.
    """)

    # Download
    ts = datetime.now().strftime("%H%M%S")
    fname = f"Exo_Group_{scen_e['tag']}_{ts}.xlsx"
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as w:
        df_e.to_excel(w, index=False)
    
    st.download_button(f"📥 Télécharger Excel ({scen_e['tag']})", out.getvalue(), fname)

    # Upload & Correction
    up_grp = st.file_uploader("Déposez le fichier Excel avec le TCD groupé", type=['xlsx'], key="up_grp")
    
    if up_grp:
        try:
            wb = openpyxl.load_workbook(up_grp, data_only=True)
            found_nums = set()
            
            # Scan global
            for s in wb.worksheets:
                for r in s.iter_rows(values_only=True):
                    for c in r:
                        if isinstance(c, (int, float)):
                            found_nums.add(int(c)) # On cherche les effectifs (entiers)
            
            # Vérité
            sol = pd.cut(df_e["Variable"], bins=scen_e["bins"], labels=scen_e["labels"], right=False)
            corr = sol.value_counts().sort_index()
            
            st.divider()
            cols = st.columns(2)
            ok = True
            
            for i, (lbl, cnt) in enumerate(corr.items()):
                with cols[i%2]:
                    # On cherche uniquement si le chiffre 'cnt' existe dans le fichier
                    # (Tolérance maximale sur le nom des étiquettes dans Excel)
                    if cnt in found_nums:
                        st.success(f"✅ Tranche {lbl} : {cnt}")
                    else:
                        st.error(f"❌ Tranche {lbl} : {cnt} introuvable")
                        ok = False
            
            # Check Total
            if len(df_e) in found_nums:
                st.success(f"✅ Total Général ({len(df_e)}) correct.")
            else:
                st.warning("⚠️ Total général introuvable.")

            if ok:
                st.balloons()
                st.success("👏 Parfait ! Vous maîtrisez le groupement Excel.")

        except Exception as e:
            st.error(f"Erreur technique : {e}")