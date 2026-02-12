import streamlit as st
import pandas as pd
import numpy as np
import io
import random

st.set_page_config(page_title="S2 | Ex7 : Moyenne Pondérée", page_icon="🎯", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=27"

st.title("🎯 S2 | Ex. 7 : La Moyenne Pondérée")

SCENARIOS = {
    "academic": {
        "titre": "Semestre (Notes x ECTS)", "l_val": "Note", "l_w": "Coef",
        "items": ["Droit", "Eco", "Histoire", "Anglais"], "min": 8, "max": 18, "w": [6, 6, 4, 3]
    },
    "market": {
        "titre": "Panier (Prix x Qty)", "l_val": "Prix", "l_w": "Qté",
        "items": ["Pâtes", "Viande", "Légumes", "Eau"], "min": 2, "max": 15, "w": [5, 2, 4, 6]
    }
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Calculer une moyenne quand les éléments n'ont pas la même importance (Poids/Coefficients).
    """)

if st.button("🔄 Nouveau Cas"):
    for k in ['wm_man_data', 'wm_man_scen', 'wm_xl_data', 'wm_xl_scen']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel", "📊 Mode Excel"])

# --- MANUEL ---
with tab_man:
    st.subheader("Calcul 'à la main'")
    
    with st.sidebar:
        st.header("📝 Aide : Pondération")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Formule :**
        $$ \\bar{{x}} = \\frac{{\\sum (x_i \\times p_i)}}{{\\sum p_i}} $$
        
        **Étapes :**
        1. Multiplier chaque Note par son Coef.
        2. Faire la somme des résultats (Numérateur).
        3. Diviser par la somme des Coefs (Dénominateur).
        """, unsafe_allow_html=True)
    
    if 'wm_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = [random.randint(scen["min"], scen["max"]) for _ in scen["items"]]
        df = pd.DataFrame({"Item": scen["items"], scen["l_val"]: vals, scen["l_w"]: scen["w"]})
        st.session_state.wm_man_data = df
        st.session_state.wm_man_scen = scen

    df_m = st.session_state.wm_man_data
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.dataframe(df_m, hide_index=True)
    with col2:
        u_res = st.number_input("Résultat :", step=0.1)
        if st.button("Vérifier"):
            num = sum(df_m.iloc[:, 1] * df_m.iloc[:, 2])
            den = sum(df_m.iloc[:, 2])
            res = num / den
            if abs(u_res - res) < 0.1:
                st.success(f"✅ Bravo ! {res:.2f}")
                st.balloons()
            else:
                st.error(f"❌ ({num} / {den}) = {res:.2f}")

# --- EXCEL ---
with tab_xl:
    st.subheader("Calcul sur données groupées")
    
    with st.sidebar:
        st.header("📊 Aide : Excel")
        st.markdown("""
        **Fonction Magique :**
        `=SOMMEPROD(Plage1; Plage2)`
        
        Cette fonction multiplie les lignes et fait la somme (le numérateur).
        
        **Formule Complète :**
        `=SOMMEPROD(Notes; Coefs) / SOMME(Coefs)`
        """)
    
    if 'wm_xl_data' not in st.session_state:
        cats = ["Ouvriers", "Employés", "Cadres", "Dirigeants"]
        eff = [random.randint(50, 200) for _ in cats]
        sal = [1600, 2000, 3500, 8000]
        st.session_state.wm_xl_data = pd.DataFrame({"Cat": cats, "Effectif": eff, "Salaire": sal})
    
    df_x = st.session_state.wm_xl_data
    
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    st.download_button("📥 Télécharger", out.getvalue(), "MQ_Ponderee.xlsx")
    
    u_val = st.number_input("Salaire Moyen Global :", step=1.0)
    if st.button("Correction"):
        res = sum(df_x["Effectif"] * df_x["Salaire"]) / sum(df_x["Effectif"])
        if abs(u_val - res) < 1:
            st.success(f"✅ Correct ! ({res:.0f})")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {res:.0f}")