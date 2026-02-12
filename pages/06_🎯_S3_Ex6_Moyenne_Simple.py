import streamlit as st
import pandas as pd
import numpy as np
import io
import random

st.set_page_config(page_title="S2 | Ex6 : Moyenne", page_icon="🎯", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=26"

st.title("🎯 S2 | Ex. 6 : La Moyenne Simple")

SCENARIOS = {
    "notes": {"titre": "Notes Étudiant", "unit": "/20", "min": 0, "max": 20, "digits": 1},
    "taille": {"titre": "Taille Basket", "unit": "cm", "min": 180, "max": 215, "digits": 0},
    "ecran": {"titre": "Temps Écran", "unit": "h", "min": 1, "max": 12, "digits": 1}
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Calculer le point d'équilibre qui prend en compte toutes les valeurs.
    """)

if st.button("🔄 Nouveau Cas"):
    for k in ['mean_man_data', 'mean_man_scen', 'mean_xl_data', 'mean_xl_scen']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel", "📊 Mode Excel"])

# --- MANUEL ---
with tab_man:
    st.subheader("Calcul petit échantillon")
    
    with st.sidebar:
        st.header("📝 Aide : Moyenne")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Formule :**
        $$ \\bar{{x}} = \\frac{{\\sum x_i}}{{N}} $$
        
        **En français :**
        (Somme de toutes les valeurs) divisé par (Nombre de valeurs).
        """, unsafe_allow_html=True)
    
    if 'mean_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = [round(random.uniform(scen["min"], scen["max"]), scen["digits"]) for _ in range(5)]
        st.session_state.mean_man_data = pd.DataFrame({f"Val ({scen['unit']})": vals})
        st.session_state.mean_man_scen = scen

    df_m = st.session_state.mean_man_data
    scen_m = st.session_state.mean_man_scen
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_m, height=230, hide_index=True)
    with col2:
        user_mean = st.number_input(f"Moyenne ({scen_m['unit']}) :", step=0.1)
        if st.button("Vérifier"):
            true_mean = df_m.iloc[:, 0].mean()
            if abs(user_mean - true_mean) < 0.05:
                st.success(f"✅ Bravo ! {true_mean:.2f}")
                st.balloons()
            else:
                st.error(f"❌ La moyenne est {true_mean:.2f}")

# --- EXCEL ---
with tab_xl:
    st.subheader("Fonction Excel")
    
    with st.sidebar:
        st.header("📊 Aide : Excel")
        st.markdown("""
        **Fonction :**
        `=MOYENNE(Plage)`
        
        *En anglais :* `=AVERAGE(Range)`
        """)
    
    if 'mean_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        data = np.random.normal((scen["max"]+scen["min"])/2, (scen["max"]-scen["min"])/6, 200)
        data = np.clip(data, scen["min"], scen["max"])
        st.session_state.mean_xl_data = pd.DataFrame({"ID": range(1, 201), "Val": np.round(data, scen["digits"])})
        st.session_state.mean_xl_scen = scen
    
    df_x = st.session_state.mean_xl_data
    
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    st.download_button("📥 Télécharger Excel", out.getvalue(), "MQ_Moyenne.xlsx")
    
    u_val = st.number_input("Résultat Excel :", step=0.01)
    if st.button("Correction"):
        t_val = df_x.iloc[:, 1].mean()
        if abs(u_val - t_val) < 0.05:
            st.success(f"✅ Correct ! ({t_val:.2f})")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {t_val:.2f}")