import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import scipy.stats as stats
from datetime import datetime

st.set_page_config(page_title="S8 | Ex. 15 : Test de Student", page_icon="📈", layout="wide")

st.title("📈 S8 | Ex. 15 : Le Test de Student (Comparaison à une norme)")

SCENARIOS = {
    "sc_po": {
        "titre": "Intentions de vote (Candidat A)", 
        "var_num": "Score (%)",
        "mu_0": 50.0,
        "sigma_base": 3.5,
        "description": "À la sortie des urnes, une équipe a constitué un échantillon d'électeurs. L'objectif est de vérifier si le score du Candidat A est significativement différent de la majorité absolue (50%)."
    },
    "education": {
        "titre": "Score de lecture (Méthode syllabique)", 
        "var_num": "Score (/100)",
        "mu_0": 50.0,
        "sigma_base": 12.0,
        "description": "Une nouvelle méthode d'apprentissage a été testée. Vous cherchez à savoir si le score moyen de ces élèves diffère de la moyenne nationale historique."
    },
    "psychologie": {
        "titre": "Temps d'écran quotidien des adolescents", 
        "var_num": "Temps (heures)",
        "mu_0": 4.5,
        "sigma_base": 1.2,
        "description": "Vous avez relevé le temps passé sur les réseaux sociaux par un panel de lycéens pour tester si cette cohorte s'écarte significativement de la norme observée il y a cinq ans."
    }
}

def generate_controlled_sample(n, mu_0, sigma, target_p):
    """Génère un échantillon qui aura (presque exactement) la p-valeur ciblée."""
    # Trouver le t théorique correspondant à la p-valeur ciblée
    target_t = stats.t.ppf(1 - target_p/2, df=n-1) * random.choice([1, -1])
    
    # Créer une distribution centrée réduite parfaite
    raw_data = np.random.normal(size=n)
    raw_data = (raw_data - np.mean(raw_data)) / np.std(raw_data, ddof=1)
    
    # Appliquer le décalage exact
    exact_shift = target_t * (sigma / np.sqrt(n))
    data = raw_data * sigma + (mu_0 + exact_shift)
    
    # On arrondit à 1 décimale (cela va très légèrement modifier la p-valeur finale, ce qui fait plus naturel)
    return np.round(data, 1).tolist()

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Vérifier si une moyenne observée dans un échantillon est statistiquement différente d'une moyenne théorique de référence ($\mu_0$).
    
    ### 🧠 Le sens de l'exercice
    Le **test de Student** permet de savoir si l'écart observé entre notre échantillon et la norme est dû au simple hasard ou s'il révèle une véritable dynamique sociologique ou comportementale.
    
    **Les hypothèses du test :**
    * **$H_0$ (Hypothèse nulle) :** La vraie moyenne est égale à la norme ($\mu = \mu_0$). Les variations de l'échantillon ne relèvent que du hasard.
    * **$H_1$ (Hypothèse alternative) :** La vraie moyenne est significativement différente ($\mu \\neq \mu_0$).
    
    **Règle de décision :**
    On rejette $H_0$ si la statistique $t$ est en dehors de l'intervalle **[-1,96 ; 1,96]** (au seuil de confiance de 95%) ou si la **p-valeur est inférieure à 5% (0,05)**.
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['stu_man_data', 'stu_xl_data', 'editor_key_stu']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** Mesurer l'écart entre notre échantillon et la théorie, en pondérant par l'incertitude (erreur-type).")
        st.latex(r"Erreur\text{-}type = \frac{s}{\sqrt{n}}")
        st.latex(r"t = \frac{\bar{x} - \mu_0}{Erreur\text{-}type}")
        st.markdown("""
        **Où :**
        * $\\bar{x}$ : Moyenne de l'échantillon
        * $\mu_0$ : Valeur théorique de référence
        * $s$ : Écart-type de l'échantillon
        * $n$ : Taille de l'échantillon
        """)
    
    if 'stu_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        n_val = random.randint(10, 15)
        # On cible des p-valeurs variées même pour le manuel
        target_p = random.choice([random.uniform(0.10, 0.60), random.uniform(0.01, 0.04)])
        data_m = generate_controlled_sample(n_val, scen["mu_0"], scen["sigma_base"], target_p)
        
        st.session_state.stu_man_data = data_m
        st.session_state.stu_man_scen = scen
    
    scen_m = st.session_state.stu_man_scen
    data_m = st.session_state.stu_man_data
    mu_0 = scen_m['mu_0']

    st.info(f"""
    **Mini-échantillon :** *{scen_m['titre']}*. 
    Nous voulons savoir si la moyenne de ce sous-groupe est significativement différente de la norme théorique **$\mu_0 = {mu_0}$**.
    """)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Données relevées")
        df_display = pd.DataFrame({scen_m['var_num']: data_m})
        st.dataframe(df_display, hide_index=True, use_container_width=True)
        
        std_sample = np.std(data_m, ddof=1)
        st.caption(f"💡 *Indice : L'écart-type de cet échantillon (s) est d'environ {std_sample:.2f}*")

    with col2:
        st.markdown("#### Étapes de calcul")
        
        u_n = st.number_input("1. Taille de l'échantillon (n) :", step=1, key="u_n")
        u_moy = st.number_input("2. Moyenne de l'échantillon ($\\bar{x}$) :", step=0.1, key="u_moy")
        u_se = st.number_input(f"3. Erreur-type ($s / \sqrt{{n}}$) :", step=0.1, key="u_se")
        u_t = st.number_input(f"4. Statistique t :", step=0.1, key="u_t")
        
        u_conclu = st.radio(
            "5. Comparaison au seuil de signification :",
            ["Sélectionner...", 
             "t est en dehors de l'intervalle [-1.96; 1.96] (Rejet de H0)", 
             "t est dans l'intervalle [-1.96; 1.96] (Non-rejet de H0)"]
        )
        
        if st.button("✅ Vérifier les calculs manuels"):
            n_m = len(data_m)
            true_mean = np.mean(data_m)
            true_se = std_sample / np.sqrt(n_m)
            true_t = (true_mean - mu_0) / true_se
            
            if true_t < -1.96 or true_t > 1.96:
                true_conclu = "t est en dehors de l'intervalle [-1.96; 1.96] (Rejet de H0)"
            else:
                true_conclu = "t est dans l'intervalle [-1.96; 1.96] (Non-rejet de H0)"
            
            erreurs = []
            if int(u_n) != n_m:
                erreurs.append(f"La taille de l'échantillon est incorrecte (Attendu : {n_m}).")
            if abs(u_moy - true_mean) > 0.1:
                erreurs.append(f"La moyenne est incorrecte (Attendu : {true_mean:.2f}).")
            if abs(u_se - true_se) > 0.1:
                erreurs.append(f"L'erreur-type est incorrecte (Attendu : {true_se:.2f}).")
            if abs(u_t - true_t) > 0.1:
                erreurs.append(f"La statistique t est incorrecte (Attendu : {true_t:.2f}).")
            if u_conclu != true_conclu and u_conclu != "Sélectionner...":
                erreurs.append(f"La conclusion est incorrecte. La vraie valeur de t est {true_t:.2f}.")
            elif u_conclu == "Sélectionner...":
                erreurs.append("Veuillez statuer sur l'hypothèse nulle.")
                
            if not erreurs:
                st.success("👏 Parfait ! Le raisonnement mathématique du test de Student est validé.")
                st.balloons()
            else:
                st.error("⚠️ Erreurs trouvées :")
                for err in erreurs:
                    st.warning(err)

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonctions et Décisions sur Excel")     
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown("""
        **Les fonctions Excel utiles :**
        
        1. `=NB(Plage)` *(Pour trouver n)*
        2. `=MOYENNE(Plage)`
        3. `=ECARTYPE.PEARSON(Plage)` *(ou STANDARD selon le corrigé)*
        4. `=RACINE(Nombre)`
        5. Calculer le t manuellement : `=(Moyenne - Theorie) / Erreur_type`
        6. La **P-valeur** avec la loi bilatérale :
        `=LOI.STUDENT.BILATERALE(ABS(t); n - 1)`
        """)
    
    if 'stu_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen_x = SCENARIOS[s_key]
        
        n_xl = random.randint(50, 80)
        
        # Sélection stratégique d'un scénario de p-valeur pour assurer la diversité de l'exercice
        scenario_type = random.choice(["non_rejet_evident", "non_rejet_limite", "rejet_limite", "rejet_evident"])
        
        if scenario_type == "non_rejet_evident":
            target_p = random.uniform(0.20, 0.80)
        elif scenario_type == "non_rejet_limite":
            target_p = random.uniform(0.06, 0.15) # p-valeur entre 6% et 15%
        elif scenario_type == "rejet_limite":
            target_p = random.uniform(0.01, 0.04) # p-valeur entre 1% et 4%
        else:
            target_p = random.uniform(0.0001, 0.005) # p-valeur très proche de 0
            
        data_xl = generate_controlled_sample(n_xl, scen_x["mu_0"], scen_x["sigma_base"], target_p)
        
        st.session_state.stu_xl_data = pd.DataFrame({scen_x["var_num"]: data_xl})
        st.session_state.stu_xl_scen = scen_x
        
        # On recalcule la vraie p-valeur après l'arrondi pour la correction
        t_stat, p_val = stats.ttest_1samp(data_xl, scen_x["mu_0"])
        st.session_state.true_pval = p_val
    
    df_x = st.session_state.stu_xl_data
    scen_x = st.session_state.stu_xl_scen
    mu_0_xl = scen_x['mu_0']
    
    st.info(f"""
    **Problématique de recherche :** {scen_x['description']} Vous analysez les données complètes de {len(df_x)} enquêtés. La moyenne théorique de référence est fixée à **$\mu_0 = {mu_0_xl}$**.
    
    **Consigne :** Téléchargez le jeu de données, calculez la statistique t, puis déterminez la **p-valeur** sur Excel. Enfin, répondez au questionnaire d'interprétation.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S8_Ex15_Student_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger la base de données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        u_pval = st.number_input("La p-valeur obtenue sur Excel (ex: 0.034 ou 0.125) :", step=0.001, format="%.3f")
        
        u_qcm_1 = st.radio(
            "Au seuil de tolérance de 5% (0,05), quelle est la décision statistique ?",
            ["Sélectionner...", "On rejette l'hypothèse nulle (H0)", "On ne rejette pas l'hypothèse nulle (H0)"]
        )
        
        u_qcm_2 = st.radio(
            "Que concluez-vous concrètement pour votre analyse ?",
            ["Sélectionner...", 
             "L'écart observé par rapport à la moyenne historique est statistiquement significatif. Il y a un véritable effet ou changement.", 
             "L'écart observé est trop faible ; il est très probablement dû au hasard de l'échantillonnage. On ne peut pas prouver de différence."]
        )
        
    if st.button("Valider l'analyse Excel"):
        true_pval = st.session_state.true_pval
        rejette_h0 = true_pval < 0.05
        
        expected_q1 = "On rejette l'hypothèse nulle (H0)" if rejette_h0 else "On ne rejette pas l'hypothèse nulle (H0)"
        expected_q2 = "L'écart observé par rapport à la moyenne historique est statistiquement significatif. Il y a un véritable effet ou changement." if rejette_h0 else "L'écart observé est trop faible ; il est très probablement dû au hasard de l'échantillonnage. On ne peut pas prouver de différence."
        
        errors_xl = []
        if abs(u_pval - true_pval) > 0.015:
            errors_xl.append(f"La p-valeur est incorrecte (attendue : ~{true_pval:.3f}). Vérifiez le calcul de t et vos degrés de liberté ({len(df_x)-1}).")
            
        if u_qcm_1 != expected_q1 and u_qcm_1 != "Sélectionner...":
            errors_xl.append("Erreur sur la décision statistique. Rappel : on rejette H0 uniquement si p-valeur < 0,05.")
        elif u_qcm_1 == "Sélectionner...":
            errors_xl.append("Veuillez statuer sur l'hypothèse nulle.")
            
        if u_qcm_2 != expected_q2 and u_qcm_2 != "Sélectionner...":
            errors_xl.append("Erreur d'interprétation finale. Une p-valeur > 0,05 signifie que le hasard reste l'explication la plus probable.")
        elif u_qcm_2 == "Sélectionner...":
            errors_xl.append("Veuillez sélectionner une conclusion de recherche.")

        if not errors_xl:
            st.success(f"✅ Excellent ! La vraie p-valeur était de {true_pval:.3f}. Ton interprétation des données est correcte.")
        else:
            st.error("❌ Certaines étapes posent problème :")
            for e in errors_xl:
                st.warning(e)