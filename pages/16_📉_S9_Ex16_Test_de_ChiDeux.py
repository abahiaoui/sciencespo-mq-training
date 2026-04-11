import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import scipy.stats as stats
from datetime import datetime

st.set_page_config(page_title="S8 | Ex. 16 : Test du Chi-deux", page_icon="📊", layout="wide")

st.title("📊 S8 | Ex. 16 : Le Test du Chi-deux (Indépendance de deux variables)")

SCENARIOS = {
    "vote_genre": {
        "titre": "Vote et Genre", 
        "var_cat1": "Genre",
        "var_cat2": "Vote",
        "labels1": ["Femme", "Homme"],
        "labels2": ["Candidat A", "Candidat B"],
        "description": "À la sortie des urnes, on cherche à vérifier si le choix du candidat est indépendant du genre de l'électeur."
    },
    "education_abstention": {
        "titre": "Diplôme et Abstention", 
        "var_cat1": "Niveau d'études",
        "var_cat2": "Comportement électoral",
        "labels1": ["Bac", "Supérieur"],
        "labels2": ["A voté", "S'est abstenu"],
        "description": "Une étude sociologique analyse si le niveau de diplôme a un lien significatif avec le fait de s'abstenir lors des élections."
    },
    "transport_csp": {
        "titre": "Transports et Profession", 
        "var_cat1": "Catégorie",
        "var_cat2": "Transport principal",
        "labels1": ["Employé", "Cadre"],
        "labels2": ["Voiture", "Transport en commun"],
        "description": "Dans le cadre d'un plan d'urbanisme, on souhaite savoir si l'usage des transports en commun dépend de la catégorie socioprofessionnelle."
    }
}

def generate_controlled_chi2_sample(n, var1, var2, labels1, labels2, scenario_type):
    """Génère un DataFrame simulant des variables catégorielles plus ou moins dépendantes."""
    p1 = random.uniform(0.4, 0.6)
    p2 = random.uniform(0.4, 0.6)
    
    probs = np.array([
        [p1 * p2, p1 * (1 - p2)],
        [(1 - p1) * p2, (1 - p1) * (1 - p2)]
    ])
    
    if scenario_type == "rejet_evident":
        shift = random.uniform(0.15, 0.25)
    elif scenario_type == "rejet_limite":
        shift = random.uniform(0.08, 0.12)
    elif scenario_type == "non_rejet_limite":
        shift = random.uniform(0.04, 0.07)
    else: 
        shift = random.uniform(0.0, 0.02)
        
    sign = random.choice([1, -1])
    probs[0, 0] += sign * shift
    probs[1, 1] += sign * shift
    probs[0, 1] -= sign * shift
    probs[1, 0] -= sign * shift
    
    probs = np.clip(probs, 0.01, 0.99)
    probs = probs / probs.sum()
    
    data = []
    flat_probs = probs.flatten()
    for _ in range(n):
        choice = np.random.choice(4, p=flat_probs)
        if choice == 0: data.append({var1: labels1[0], var2: labels2[0]})
        elif choice == 1: data.append({var1: labels1[0], var2: labels2[1]})
        elif choice == 2: data.append({var1: labels1[1], var2: labels2[0]})
        else: data.append({var1: labels1[1], var2: labels2[1]})
        
    return pd.DataFrame(data)

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Déterminer si deux variables catégorielles (ex: le genre et le vote) sont indépendantes ou s'il existe un lien statistique significatif entre elles.
    
    ### 🧠 Le sens de l'exercice
    Le **Test du Chi-deux ($\chi^2$)** compare les effectifs *observés* dans notre échantillon avec les effectifs *théoriques* que l'on aurait obtenus s'il n'y avait absolument aucun lien entre les variables.
    
    **Les hypothèses du test :**
    * **$H_0$ (Hypothèse nulle) :** Indépendance totale. Les variables n'ont aucun lien. Les écarts observés ne sont dus qu'au hasard.
    * **$H_1$ (Hypothèse alternative) :** Dépendance. Il existe une relation significative entre les deux variables.
    
    **Règle de décision :**
    On rejette $H_0$ si la **p-valeur est inférieure à 5% (0,05)**.
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['chi_man_data', 'chi_xl_data', 'editor_key_chi']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** Comparer la réalité (O) à la théorie (E).")
        st.markdown("**1. Calcul de l'effectif théorique (E) :**")
        st.latex(r"E = \frac{TotalLigne \times TotalColonne}{TotalGlobal}")
        st.markdown("**2. Calcul de la statistique Chi-deux :**")
        st.latex(r"\chi^2 = \sum \frac{(O - E)^2}{E}")
        st.markdown("""
        *(La somme se fait sur toutes les cases du tableau croisé, hors totaux).*
        """)
    
    if 'chi_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        n_val = random.randint(80, 150)
        scenario_type = random.choice(["non_rejet_evident", "rejet_evident"])
        df_m = generate_controlled_chi2_sample(n_val, scen["var_cat1"], scen["var_cat2"], scen["labels1"], scen["labels2"], scenario_type)
        
        tab_obs = pd.crosstab(df_m[scen["var_cat1"]], df_m[scen["var_cat2"]], margins=True, margins_name="Total")
        
        st.session_state.chi_man_data = tab_obs
        st.session_state.chi_man_scen = scen
        st.session_state.chi_man_raw = df_m
    
    if 'editor_key_chi' not in st.session_state:
        st.session_state.editor_key_chi = random.randint(0, 100000)
    
    scen_m = st.session_state.chi_man_scen
    tab_obs = st.session_state.chi_man_data
    df_raw_m = st.session_state.chi_man_raw

    st.info(f"""
    **Mini-échantillon :** *{scen_m['titre']}*. 
    Le tableau ci-dessous présente les effectifs observés (O) de notre enquête. Construisez le tableau théorique (E) attendu en cas d'indépendance parfaite, puis déduisez-en le $\chi^2$.
    """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### Effectifs Observés (O)")
        st.dataframe(tab_obs, use_container_width=True)
        
        # Précalcul du chi-deux réel pour la correction
        tab_core = pd.crosstab(df_raw_m[scen_m["var_cat1"]], df_raw_m[scen_m["var_cat2"]])
        chi2_stat, p_val, dof, ex = stats.chi2_contingency(tab_core, correction=False)
        st.caption(f"💡 *Indice : La statistique $\chi^2$ finale est d'environ {chi2_stat:.2f}*")

    with col2:
        st.markdown("#### 1. Effectifs Théoriques (E)")
        
        # Préparation du dataframe vide pour le st.data_editor
        df_theo_input = pd.DataFrame(columns=[scen_m["var_cat1"]] + scen_m["labels2"])
        df_theo_input[scen_m["var_cat1"]] = scen_m["labels1"]
        for col in scen_m["labels2"]:
            df_theo_input[col] = [None] * len(scen_m["labels1"])
        
        edited_theo = st.data_editor(
            df_theo_input,
            column_config={
                scen_m["var_cat1"]: st.column_config.TextColumn(disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            key=f"editor_chi_{st.session_state.editor_key_chi}"
        )
        
        st.markdown("#### 2. Statistique et Conclusion")
        u_chi2 = st.number_input("Somme de la statistique $\chi^2$ globale :", step=0.01, key="u_chi2")
        
        # Calcul dynamique de la p-valeur en fonction de l'input de l'étudiant (ddl = 1 pour un tableau 2x2)
        user_pval_dynamic = stats.chi2.sf(u_chi2, df=1) if u_chi2 >= 0 else 1.0
        
        if u_chi2 > 0:
            st.info(f"👉 D'après votre calcul de $\chi^2$, la p-valeur correspondante est de **{user_pval_dynamic:.4f}**.")
        
        u_conclu = st.radio(
            "Sachant que le seuil de tolérance est de 5% (0,05), quelle est votre décision ?",
            ["Sélectionner...", 
             "La p-valeur est < 0,05 (Rejet de H0 : Il y a un lien)", 
             "La p-valeur est >= 0,05 (Non-rejet de H0 : Indépendance)"]
        )
        
        if st.button("✅ Vérifier les calculs manuels"):
            erreurs = []
            
            # Vérification de la grille théorique
            for i, row_label in enumerate(scen_m["labels1"]):
                for j, col_label in enumerate(scen_m["labels2"]):
                    user_val = edited_theo.loc[i, col_label]
                    true_val = ex[i, j]
                    
                    if pd.isnull(user_val):
                        erreurs.append(f"Veuillez remplir la case [{row_label}, {col_label}].")
                    else:
                        try:
                            if abs(float(user_val) - true_val) > 0.5:
                                erreurs.append(f"Erreur sur la case [{row_label}, {col_label}] (Attendu : ~{true_val:.1f}). Vérifiez la formule : Total Ligne × Total Colonne / Total Global.")
                        except ValueError:
                            erreurs.append(f"La valeur dans la case [{row_label}, {col_label}] doit être un nombre.")

            # Vérification du Chi2 et de la conclusion
            if abs(u_chi2 - chi2_stat) > 0.2:
                erreurs.append(f"La statistique Chi-deux globale est incorrecte (Attendue : ~{chi2_stat:.2f}). N'oubliez pas de sommer (O-E)²/E pour les 4 cases.")
                
            if p_val < 0.05:
                true_conclu = "La p-valeur est < 0,05 (Rejet de H0 : Il y a un lien)"
            else:
                true_conclu = "La p-valeur est >= 0,05 (Non-rejet de H0 : Indépendance)"
                
            if u_conclu != true_conclu and u_conclu != "Sélectionner...":
                erreurs.append("La conclusion est incorrecte par rapport à votre p-valeur et au seuil de 0,05.")
            elif u_conclu == "Sélectionner...":
                erreurs.append("Veuillez statuer sur l'hypothèse nulle.")
                
            if not erreurs:
                st.success("👏 Parfait ! Vous maîtrisez la construction du tableau théorique, le calcul du Chi-deux et l'interprétation de la p-valeur.")
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
        **Procédure Excel :**
        
        1. **Tableau Observé (O)** : Faites un Tableau Croisé Dynamique avec vos deux variables.
        2. **Tableau Théorique (E)** : Copiez la structure du TCD, et appliquez la formule `=Ligne*Colonne/Global` pour chaque case.
        3. **Le $\chi^2$ par case** : Calculez l'écart pour chaque croisement avec la formule `=(O - E)^2 / E`.
        4. **$\chi^2$ Total** : Faites la somme de ces écarts.
        5. **La P-valeur** : 
        `=LOI.KHIDEUX.DROITE(Chi2_total; ddl)`
        *(Rappel : ddl = (L-1) × (C-1) pour un tableau L×C).*
        """)
    
    if 'chi_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen_x = SCENARIOS[s_key]
        
        n_xl = random.randint(200, 400) 
        scenario_type = random.choice(["non_rejet_evident", "non_rejet_limite", "rejet_limite", "rejet_evident"])
            
        df_xl = generate_controlled_chi2_sample(n_xl, scen_x["var_cat1"], scen_x["var_cat2"], scen_x["labels1"], scen_x["labels2"], scenario_type)
        
        st.session_state.chi_xl_data = df_xl
        st.session_state.chi_xl_scen = scen_x
        
        tab_core_xl = pd.crosstab(df_xl[scen_x["var_cat1"]], df_xl[scen_x["var_cat2"]])
        chi2_stat_xl, p_val_xl, dof_xl, ex_xl = stats.chi2_contingency(tab_core_xl, correction=False)
        st.session_state.true_chi_xl = chi2_stat_xl
        st.session_state.true_pval_chi = p_val_xl
    
    df_x = st.session_state.chi_xl_data
    scen_x = st.session_state.chi_xl_scen
    
    st.info(f"""
    **Problématique de recherche :** {scen_x['description']} Vous analysez les réponses brutes de {len(df_x)} individus.
    
    **Consigne :** Téléchargez le jeu de données. Sur Excel, calculez le $\chi^2$ total case par case, puis utilisez la fonction `LOI.KHIDEUX.DROITE` pour obtenir la p-valeur.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S8_Ex16_Chideux_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger la base de données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        u_chi2_xl = st.number_input("La statistique $\chi^2$ totale obtenue :", step=0.01, format="%.2f", key="u_chi2_xl")
        u_pval = st.number_input("La p-valeur issue de LOI.KHIDEUX.DROITE (ex: 0.034) :", step=0.001, format="%.3f", key="u_pval_xl")
        
        u_qcm_1 = st.radio(
            "Au seuil de tolérance de 5% (0,05), quelle est la décision statistique ?",
            ["Sélectionner...", "On rejette l'hypothèse nulle (H0)", "On ne rejette pas l'hypothèse nulle (H0)"],
            key="u_q1_xl"
        )
        
        u_qcm_2 = st.radio(
            "Que concluez-vous sociologiquement ?",
            ["Sélectionner...", 
             "Les deux variables sont statistiquement liées. L'une influence probablement l'autre.", 
             "L'écart entre les profils est trop faible. Les variables sont indépendantes (ou l'échantillon ne permet pas de prouver le contraire)."],
            key="u_q2_xl"
        )
        
    if st.button("Valider l'analyse Excel", key="btn_xl"):
        true_chi = st.session_state.true_chi_xl
        true_pval = st.session_state.true_pval_chi
        rejette_h0 = true_pval < 0.05
        
        expected_q1 = "On rejette l'hypothèse nulle (H0)" if rejette_h0 else "On ne rejette pas l'hypothèse nulle (H0)"
        expected_q2 = "Les deux variables sont statistiquement liées. L'une influence probablement l'autre." if rejette_h0 else "L'écart entre les profils est trop faible. Les variables sont indépendantes (ou l'échantillon ne permet pas de prouver le contraire)."
        
        errors_xl = []
        if abs(u_chi2_xl - true_chi) > 0.2:
            errors_xl.append(f"La statistique $\chi^2$ totale est incorrecte (attendue : ~{true_chi:.2f}). Revérifiez la somme des (O-E)²/E.")
            
        if abs(u_pval - true_pval) > 0.015:
            errors_xl.append(f"La p-valeur est incorrecte (attendue : ~{true_pval:.3f}). Avez-vous bien utilisé =LOI.KHIDEUX.DROITE(chi2; 1) ?")
            
        if u_qcm_1 != expected_q1 and u_qcm_1 != "Sélectionner...":
            errors_xl.append("Erreur sur la décision statistique. Rappel : on rejette H0 uniquement si p-valeur < 0,05.")
        elif u_qcm_1 == "Sélectionner...":
            errors_xl.append("Veuillez statuer sur l'hypothèse nulle.")
            
        if u_qcm_2 != expected_q2 and u_qcm_2 != "Sélectionner...":
            errors_xl.append("Erreur d'interprétation finale. Si H0 est rejetée, il y a un lien (dépendance). Sinon, on conclut à l'indépendance.")
        elif u_qcm_2 == "Sélectionner...":
            errors_xl.append("Veuillez sélectionner une conclusion de recherche.")

        if not errors_xl:
            st.success(f"✅ Excellent ! Le $\chi^2$ était bien de {true_chi:.2f} (p-valeur de {true_pval:.3f}). L'interprétation des liens entre ces variables est parfaite.")
        else:
            st.error("❌ Certaines étapes posent problème :")
            for e in errors_xl:
                st.warning(e)