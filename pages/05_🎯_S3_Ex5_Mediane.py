import streamlit as st
import pandas as pd
import numpy as np
import io
import random

st.set_page_config(page_title="S2 | Ex5 : Médiane", page_icon="🎯", layout="wide")

# --- URL SLIDES (A ajuster selon votre repo) ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=29"

st.title("🎯 S2 | Ex. 5 : La Médiane")

SCENARIOS = {
    "salaires": {
        "titre": "Salaires Start-up", "unit": "€", "min": 1500, "max": 2500, "step": 50,
        "outlier_min": 12000, "outlier_max": 25000, "label": "Salaire"
    },
    "immo": {
        "titre": "Prix Immobilier", "unit": "k€", "min": 200, "max": 400, "step": 10,
        "outlier_min": 2000, "outlier_max": 5000, "label": "Prix"
    },
    "social": {
        "titre": "Abonnés Instagram", "unit": "abonnés", "min": 100, "max": 800, "step": 1,
        "outlier_min": 50000, "outlier_max": 1000000, "label": "Abonnés"
    }
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Trouver la valeur centrale qui sépare la population en deux moitiés égales.
    
    ### 📖 Pourquoi la médiane ?
    Contrairement à la moyenne, la médiane n'est pas influencée par les valeurs extrêmes (outliers). C'est l'indicateur du "niveau de vie standard".
    """)

if st.button("🔄 Nouveau Cas"):
    for key in ['med_data', 'med_scen', 'med_xl_data', 'med_xl_scen']:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.header("📝 Aide : Médiane")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Méthode :**
        1. **TRIER** la liste du plus petit au plus grand.
        2. Prendre la valeur du milieu.
        
        *Astuce :* Si N est impair, le rang est $(N+1)/2$.
        """, unsafe_allow_html=True)
    
    if 'med_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = [random.randrange(scen["min"], scen["max"], scen["step"]) for _ in range(8)]
        vals.append(random.randrange(scen["outlier_min"], scen["outlier_max"], scen["step"]))
        random.shuffle(vals)
        st.session_state.med_data = pd.DataFrame({scen["label"]: vals})
        st.session_state.med_scen = scen

    df_m = st.session_state.med_data
    scen_m = st.session_state.med_scen

    st.info(f"**{scen_m['titre']}**. Voici 9 valeurs en vrac. Trouvez la médiane.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_m, height=350, hide_index=True)
    with col2:
        user_med = st.number_input(f"Médiane ({scen_m['unit']}) :", step=scen_m['step'])
        if st.button("✅ Vérifier", key="chk_med"):
            sorted_vals = sorted(df_m[scen_m["label"]].tolist())
            true_med = sorted_vals[4]
            st.write(f"**Données triées :** {sorted_vals}")
            if user_med == true_med:
                st.success(f"👏 Bravo ! C'est bien {true_med}.")
                st.balloons()
            else:
                st.error(f"❌ Faux. Une fois trié, le 5ème élément est {true_med}.")

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📊 Aide : Excel")
        st.markdown("""
        **Fonction :**
        `=MEDIANE(Plage)`
        
        *En anglais :* `=MEDIAN(Range)`
        
        ⚠️ Ne sélectionnez pas les entêtes, juste les chiffres !
        """)
    
    if 'med_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        data = np.random.lognormal(mean=np.log(scen["min"]), sigma=0.8, size=500)
        data = np.round(data / scen["step"]) * scen["step"]
        data = data[data > scen["min"] / 2]
        st.session_state.med_xl_data = pd.DataFrame({"ID": range(1, len(data)+1), scen["label"]: data})
        st.session_state.med_xl_scen = scen
    
    df_x = st.session_state.med_xl_data
    scen_x = st.session_state.med_xl_scen
    
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    st.download_button("📥 Télécharger Données", out.getvalue(), f"MQ_Mediane.xlsx")
    
    u_val = st.number_input(f"Résultat Excel ({scen_x['unit']}) :", step=1.0)
    if st.button("Correction"):
        t_val = df_x[scen_x["label"]].median()
        if abs(u_val - t_val) < 1:
            st.success(f"✅ Correct ! ({t_val})")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {t_val}")