import streamlit as st
import pandas as pd
import numpy as np
import io
import random

st.set_page_config(page_title="S3 | Ex1 : Dispersion", page_icon="📉", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=40"

st.title("📉 S3 | Ex. 1 : Variance & Écart-Type")

SCENARIOS = {
    "notes": {
        "titre": "Notes (Régularité)", "unit": "/20",
        "vals_a": [11, 12, 12, 13, 12], "vals_b": [6, 18, 5, 19, 12], "mean": 12
    }
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Mesurer la dispersion : les données sont-elles serrées (homogènes) ou étalées (hétérogènes) autour de la moyenne ?
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['var_man_data', 'var_xl_data']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel", "📊 Mode Excel"])

# --- MANUEL ---
with tab_man:
    st.subheader("Décomposition du calcul")
    
    with st.sidebar:
        st.header("📝 Aide : Variance")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Algorithme :**
        1. **Moyenne** ($\mu$).
        2. **Écarts :** $(x_i - \mu)$.
        3. **Carrés :** $(x_i - \mu)^2$ (Toujours positif !).
        4. **Somme des Carrés** (SCE).
        5. **Variance :** $SCE / N$.
        6. **Écart-Type :** $\sqrt{{Variance}}$.
        """, unsafe_allow_html=True)
    
    if 'var_man_data' not in st.session_state:
        scen = SCENARIOS["notes"]
        vals = random.choice([scen["vals_a"], scen["vals_b"]])
        st.session_state.var_man_data = pd.DataFrame({"Note": vals})

    df_m = st.session_state.var_man_data
    mean_val = 12
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(df_m, hide_index=True)
        st.write(f"**Moyenne = {mean_val}**")
    with col2:
        u_sse = st.number_input("1. Somme des Carrés (SCE) :", step=1.0)
        u_var = st.number_input("2. Variance ($V$) :", step=0.1)
        u_std = st.number_input("3. Écart-Type ($\sigma$) :", step=0.1)
        
        if st.button("Vérifier"):
            sce = sum((df_m["Note"] - mean_val)**2)
            var = sce / 5
            std = np.sqrt(var)
            
            if abs(u_std - std) < 0.1:
                st.success(f"✅ Correct ! Ecart-type = {std:.2f}")
                st.balloons()
            else:
                st.error(f"❌ SCE={sce}, Var={var}, Std={std:.2f}")

# --- EXCEL ---
with tab_xl:
    st.subheader("Fonctions Excel")
    
    with st.sidebar:
        st.header("📊 Aide : Excel")
        st.markdown("""
        **Attention :** Il existe deux versions des formules.
        
        * **Population (Ce qu'on veut) :**
            `=VAR.P(Plage)`
            `=ECARTYPE.P(Plage)`
            *(Divise par N)*
            
        * Échantillon (Sondages) :
            `=VAR.S(Plage)`
            *(Divise par N-1)*
            
        👉 Utilisez toujours **.P** dans ce cours.
        """)
    
    if 'var_xl_data' not in st.session_state:
        stable = np.random.normal(10, 2, 100)
        dispersed = np.random.normal(10, 8, 100)
        st.session_state.var_xl_data = pd.DataFrame({"Stable": np.round(stable, 1), "Dispersé": np.round(dispersed, 1)})
    
    df_x = st.session_state.var_xl_data
    
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    st.download_button("📥 Télécharger Données", out.getvalue(), "MQ_Dispersion.xlsx")
    
    colA, colB = st.columns(2)
    with colA:
        std_A = st.number_input("Écart-type Stable :", step=0.1)
    with colB:
        std_B = st.number_input("Écart-type Dispersé :", step=0.1)
        
    if st.button("Correction Excel"):
        tA = np.std(df_x["Stable"])
        tB = np.std(df_x["Dispersé"])
        if abs(std_A - tA) < 0.2 and abs(std_B - tB) < 0.2:
            st.success("✅ Correct !")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {tA:.2f} et {tB:.2f}")