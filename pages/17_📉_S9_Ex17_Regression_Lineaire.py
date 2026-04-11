import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import scipy.stats as stats
from datetime import datetime

st.set_page_config(page_title="S9 | Ex. 17 : Régression Linéaire", page_icon="📈", layout="wide")

st.title("📈 S9 | Ex. 17 : La Régression Linéaire Simple (Lecture et Prédiction)")

SCENARIOS = {
    "education": {
        "titre": "Impact du temps de révision sur la note", 
        "var_x": "Heures de révision",
        "var_y": "Note à l'examen (/20)",
        "x_mean": 15, "x_std": 5,
        "beta0_base": 5.0, "beta1_base": 0.5, "noise": 2.0,
        "pred_x": 20,
        "description": "Une étude cherche à modéliser la note obtenue à un examen en fonction du nombre d'heures passées à réviser."
    },
    "sociologie": {
        "titre": "Impact de l'expérience sur le salaire", 
        "var_x": "Années d'expérience",
        "var_y": "Salaire annuel (k€)",
        "x_mean": 10, "x_std": 6,
        "beta0_base": 28.0, "beta1_base": 1.2, "noise": 4.0,
        "pred_x": 5,
        "description": "En sociologie du travail, on modélise le salaire annuel d'un panel d'employés en fonction de leur ancienneté."
    },
    "psychologie": {
        "titre": "Stress et Qualité du sommeil", 
        "var_x": "Indice de stress (0-100)",
        "var_y": "Heures de sommeil",
        "x_mean": 60, "x_std": 15,
        "beta0_base": 9.5, "beta1_base": -0.04, "noise": 0.8,
        "pred_x": 80,
        "description": "Une enquête en psychologie évalue l'impact du niveau de stress quotidien sur la durée du sommeil."
    }
}

def generate_regression_tables(n, scen):
    """Génère les 3 tableaux standards d'une régression (Statistiques, ANOVA, Coefficients)."""
    # 1. Génération des données sous-jacentes
    x = np.random.normal(scen["x_mean"], scen["x_std"], n)
    x = np.clip(x, 0, None) # Pas de valeurs négatives
    
    # Rendre la relation plus ou moins forte (p-valeurs variées)
    shift_noise = random.uniform(0.5, 2.0) * scen["noise"]
    y = scen["beta0_base"] + scen["beta1_base"] * x + np.random.normal(0, shift_noise, n)
    
    # 2. Calculs statistiques
    slope, intercept, r_value, p_value, std_err_slope = stats.linregress(x, y)
    r_squared = r_value**2
    adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 2)
    
    # Composantes ANOVA
    ss_tot = np.var(y, ddof=1) * (n - 1)
    ss_reg = r_squared * ss_tot
    ss_res = ss_tot - ss_reg
    ms_reg = ss_reg / 1
    ms_res = ss_res / (n - 2)
    f_stat = ms_reg / ms_res
    p_f = stats.f.sf(f_stat, 1, n - 2)
    standard_error_model = np.sqrt(ms_res)
    
    # Erreurs types des coefficients
    std_err_intercept = std_err_slope * np.sqrt(np.mean(x**2))
    t_intercept = intercept / std_err_intercept
    p_intercept = 2 * stats.t.sf(np.abs(t_intercept), n - 2)
    
    # Intervalles de confiance
    t_crit = stats.t.ppf(0.975, n - 2)
    ci_int_low = intercept - t_crit * std_err_intercept
    ci_int_high = intercept + t_crit * std_err_intercept
    ci_slope_low = slope - t_crit * std_err_slope
    ci_slope_high = slope + t_crit * std_err_slope

    # 3. Formatage des tableaux (Style Excel/SPSS)
    df_stats = pd.DataFrame({
        "Statistiques de la régression": ["Coefficient de corrélation multiple", "Coefficient de détermination R^2", "R^2 ajusté", "Erreur type", "Observations"],
        "Valeur": [np.abs(r_value), r_squared, adj_r_squared, standard_error_model, n]
    })
    
    df_anova = pd.DataFrame({
        "ANOVA": ["Régression", "Résidus", "Total"],
        "Degrés de liberté (ddl)": [1, n - 2, n - 1],
        "Somme des carrés": [ss_reg, ss_res, ss_tot],
        "Moyenne des carrés": [ms_reg, ms_res, np.nan],
        "Statistique F": [f_stat, np.nan, np.nan],
        "Valeur critique de F (Signification)": [p_f, np.nan, np.nan]
    })
    
    df_coeffs = pd.DataFrame({
        "Variables": ["Constante (Intercepte)", scen["var_x"]],
        "Coefficients": [intercept, slope],
        "Erreur type": [std_err_intercept, std_err_slope],
        "Statistique t": [t_intercept, intercept / std_err_intercept], # Note: Correction stat t
        "Valeur p": [p_intercept, p_value],
        "Borne inférieure 95%": [ci_int_low, ci_slope_low],
        "Borne supérieure 95%": [ci_int_high, ci_slope_high]
    })
    df_coeffs.loc[1, "Statistique t"] = slope / std_err_slope # Fix stat t for slope
    
    return df_stats, df_anova, df_coeffs, intercept, slope, r_squared, p_value

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Savoir lire et extraire les informations pertinentes d'un rapport de **Régression Linéaire** brut généré par un logiciel statistique, puis utiliser ces résultats pour formuler une prédiction.
    
    ### 🧠 Le sens de l'exercice
    Dans le monde professionnel, vous ne ferez pas les calculs à la main. Un logiciel (Excel, R, Python, SPSS) vous renverra un tableau exhaustif (et souvent indigeste). Vous devez savoir y repérer :
    1. **Le pouvoir explicatif du modèle** : Le $R^2$ (Coefficient de détermination). Il indique le pourcentage de variance de $Y$ expliqué par $X$.
    2. **L'équation du modèle** : Pour prédire une valeur, on utilise la formule : 
    $$\hat{Y} = Coefficient_{Constante} + (Coefficient_{Variable} \times X)$$
    3. **La significativité** : La **Valeur p** (p-value) associée à la variable $X$. Si $p < 0,05$, l'impact de $X$ sur $Y$ est statistiquement significatif.
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['reg_data', 'reg_scen']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- GENERATION DES DONNEES ---
if 'reg_data' not in st.session_state:
    s_key = random.choice(list(SCENARIOS.keys()))
    scen = SCENARIOS[s_key]
    n_val = random.randint(50, 150)
    
    df_stats, df_anova, df_coeffs, b0, b1, r2, p_val = generate_regression_tables(n_val, scen)
    
    st.session_state.reg_scen = scen
    st.session_state.reg_data = {
        "stats": df_stats, "anova": df_anova, "coeffs": df_coeffs,
        "b0": b0, "b1": b1, "r2": r2, "p_val": p_val
    }

scen_m = st.session_state.reg_scen
data_m = st.session_state.reg_data

# --- MANUEL ---
with tab_man:
    st.subheader("1. Lecture du rapport d'analyse")
    
    st.info(f"""
    **Problématique :** {scen_m['description']}
    Le logiciel statistique a analysé les données et vous a renvoyé les trois tableaux ci-dessous. **Votre mission est de filtrer l'information utile.**
    """)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### Sortie du logiciel (Output)")
        st.dataframe(data_m["stats"].style.format({"Valeur": "{:.4f}"}), hide_index=True, use_container_width=True)
        st.dataframe(data_m["anova"].style.format(precision=4, na_rep=""), hide_index=True, use_container_width=True)
        st.dataframe(data_m["coeffs"].style.format(precision=4), hide_index=True, use_container_width=True)

    with col2:
        st.markdown("#### Exploitation des résultats")
        
        st.markdown("**A. Qualité du modèle**")
        u_r2 = st.number_input("1. Quel est le coefficient de détermination ($R^2$) ?", step=0.001, format="%.4f", key="u_r2")
        
        st.markdown("**B. L'équation de prédiction**")
        u_b0 = st.number_input("2. Quelle est la valeur de la Constante ($\\beta_0$) ?", step=0.01, format="%.4f", key="u_b0")
        u_b1 = st.number_input(f"3. Quel est le coefficient associé à '{scen_m['var_x']}' ($\\beta_1$) ?", step=0.01, format="%.4f", key="u_b1")
        
        pred_x = scen_m['pred_x']
        u_pred = st.number_input(f"4. En utilisant ces coefficients, prédissez la valeur de **{scen_m['var_y']}** pour un cas où {scen_m['var_x']} = **{pred_x}** :", step=0.1, format="%.2f", key="u_pred")
        
        st.markdown("**C. Décision statistique**")
        u_conclu = st.radio(
            f"Au seuil de 5%, la variable '{scen_m['var_x']}' a-t-elle un impact significatif ?",
            ["Sélectionner...", "Oui (p-valeur < 0,05)", "Non (p-valeur >= 0,05)"]
        )
        
        if st.button("✅ Vérifier mes réponses"):
            erreurs = []
            
            # Vérifications
            if abs(u_r2 - data_m["r2"]) > 0.005:
                erreurs.append("Le R² est incorrect. Cherchez la ligne 'Coefficient de détermination R^2' dans le premier tableau.")
            if abs(u_b0 - data_m["b0"]) > 0.05:
                erreurs.append("La Constante est incorrecte. Regardez la colonne 'Coefficients' dans le troisième tableau.")
            if abs(u_b1 - data_m["b1"]) > 0.05:
                erreurs.append(f"Le coefficient de {scen_m['var_x']} est incorrect. Regardez la ligne de la variable dans le troisième tableau.")
                
            true_pred = data_m["b0"] + (data_m["b1"] * pred_x)
            if abs(u_pred - true_pred) > 0.5:
                erreurs.append(f"La prédiction est incorrecte (Attendue : ~{true_pred:.2f}). Calculez : Constante + (Coefficient × {pred_x}).")
                
            expected_conclu = "Oui (p-valeur < 0,05)" if data_m["p_val"] < 0.05 else "Non (p-valeur >= 0,05)"
            if u_conclu != expected_conclu and u_conclu != "Sélectionner...":
                erreurs.append("La conclusion sur la significativité est incorrecte. Regardez la 'Valeur p' sur la ligne de la variable.")
            elif u_conclu == "Sélectionner...":
                erreurs.append("Veuillez sélectionner une conclusion.")
                
            if not erreurs:
                st.success("👏 Parfait ! Vous savez parfaitement isoler et interpréter les éléments clés d'un tableau de régression complexe.")
                st.balloons()
            else:
                st.error("⚠️ Erreurs trouvées :")
                for err in erreurs:
                    st.warning(err)

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Rapport généré via l'Ampli de Données Excel")     
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown("""
        **Comprendre la sortie Excel (Data Analysis) :**
        
        * **Statistiques de la régression** : Contient le $R^2$ qui indique la part de variance expliquée.
        * **Tableau ANOVA** : Permet de vérifier la validité globale du modèle (Signification F).
        * **Tableau des Coefficients** : 
            * **Coefficients** : Donne les valeurs de l'équation $Y = aX + b$.
            * **Valeur p (Probabilité)** : Permet de tester $H_0$ (Le coefficient est nul). Si $p < 0,05$, la variable est significative.
        """)
    
    st.info(f"""
    **Mission :** Vous recevez par e-mail le fichier de résultats Excel brut généré par le département Data.
    Téléchargez le fichier, ouvrez-le, repérez l'équation du modèle et répondez aux questions métiers.
    """)

    # Génération du fichier Excel formaté
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        data_m["stats"].to_excel(writer, sheet_name="Rapport Regression", index=False, startrow=0)
        data_m["anova"].to_excel(writer, sheet_name="Rapport Regression", index=False, startrow=4)
        data_m["coeffs"].to_excel(writer, sheet_name="Rapport Regression", index=False, startrow=12)
        
        # Ajustement esthétique de la largeur des colonnes
        worksheet = writer.sheets["Rapport Regression"]
        worksheet.set_column('A:A', 35)
        worksheet.set_column('B:G', 15)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S9_Ex17_Rapport_Regression_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger le Rapport Excel brut ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        new_pred_x = pred_x * 1.5 # Une autre valeur pour cet exercice
        u_pred_xl = st.number_input(f"1. En utilisant l'équation présente dans l'Excel, prédissez la valeur de **{scen_m['var_y']}** pour un {scen_m['var_x']} de **{new_pred_x}** :", step=0.1, format="%.2f", key="u_pred_xl")
        
        u_pval_xl = st.number_input("2. Quelle est la p-valeur (Valeur p) exacte de la variable explicative ?", step=0.0001, format="%.4f", key="u_pval_xl")
        
        u_qcm_xl = st.radio(
            "3. Comment interprétez-vous le R² affiché dans ce document ?",
            ["Sélectionner...", 
             f"Il indique que {data_m['r2']*100:.1f}% de la variance de '{scen_m['var_y']}' est expliquée par le modèle.", 
             f"Il indique que la probabilité de se tromper en utilisant ce modèle est de {data_m['r2']*100:.1f}%.",
             f"Il indique que l'impact de '{scen_m['var_x']}' augmente Y de {data_m['r2']:.2f} unités."],
            key="u_qcm_xl"
        )
        
    if st.button("Valider l'analyse", key="btn_xl"):
        true_pred_xl = data_m["b0"] + (data_m["b1"] * new_pred_x)
        expected_qcm = f"Il indique que {data_m['r2']*100:.1f}% de la variance de '{scen_m['var_y']}' est expliquée par le modèle."
        
        errors_xl = []
        if abs(u_pred_xl - true_pred_xl) > 0.5:
            errors_xl.append(f"La prédiction est incorrecte (Attendue : ~{true_pred_xl:.2f}).")
            
        if abs(u_pval_xl - data_m["p_val"]) > 0.005:
            errors_xl.append(f"La p-valeur est incorrecte. Assurez-vous de lire la 'Valeur p' sur la ligne '{scen_m['var_x']}' du tableau des coefficients.")
            
        if u_qcm_xl != expected_qcm and u_qcm_xl != "Sélectionner...":
            errors_xl.append("L'interprétation du R² est fausse. Le R² (Coefficient de détermination) mesure la proportion de variance expliquée, et non l'effet ou la marge d'erreur.")
        elif u_qcm_xl == "Sélectionner...":
            errors_xl.append("Veuillez sélectionner une interprétation pour le R².")

        if not errors_xl:
            st.success("✅ Excellent ! Vous êtes capable d'exploiter en autonomie un rapport de régression issu d'un tableur ou d'un logiciel spécialisé.")
        else:
            st.error("❌ Certaines étapes posent problème :")
            for e in errors_xl:
                st.warning(e)