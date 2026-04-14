# version 2.4 - 04/13/2026
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import logging
import os
import csv
from datetime import datetime
from src import model_load

# 1. LOGGING CONFIGURATION
logging.basicConfig(
    filename='invq_v2.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. CACHED MODEL LOADING
@st.cache_resource
def get_model():
    try:
        return model_load.load_from_pickle('scf_xgb_model.pkl')
    except Exception as e:
        st.error(f"Model Load Failed: {e}")
        return None

loaded_model = get_model()

# 3. SESSION STATE INITIALIZATION
for key in ['stage', 'total_weight', 'model_risk', 'xgb_input_df', 'client_id', 'client_name']:
    if key not in st.session_state:
        st.session_state[key] = 1 if key == 'stage' else (0.0 if key == 'total_weight' else None)

st.set_page_config(page_title="Invq Tool", page_icon="📈", layout="wide")

def Main_App():
    main_container = st.container(border=True)
    main_container.title("Investor Questionnaire Tool")

    tab_personal_info, tab_questions, tab_results = main_container.tabs([
        "Personal Information", "Questionnaire", "Risk Assessment Results"
    ])

    # --- TAB 1: PERSONAL INFORMATION ---
    with tab_personal_info:
        st.header("Personal Information")
        with st.form("info_form"):
            col1, col2 = st.columns(2)
            with col1:
                client_id_input = st.text_input("Client Number", value="001")
                client_name_input = st.text_input("Full Name")
                age = st.number_input("Age", 18, 100, 35)
                income = st.slider("Annual Household Income", 0, 500000, 50000, step=1000)
                edcl = st.selectbox("Education Level", options=[1,2,3,4])
                married = st.selectbox("Marital Status", options=[1,2])
            with col2:
                kids = st.number_input("Number of Children", 0, 10, 0)
                sex = st.selectbox("Gender", options=[1,2])
                knw = st.slider("Financial Knowledge Group", 1, 3, 2)
                occ = st.selectbox("Occupation Category", options=[1,2,3,4])
                fam = st.selectbox("Family Structure", options=[1,2,3,4,5])
                assets = st.number_input("Total Assets", 0, 10000000, 100000)
                debt = st.number_input("Total Debt", 0, 10000000, 20000)

            if st.form_submit_button("Submit and Proceed"):
                agecl = 1 if age < 35 else 2 if age < 45 else 3 if age < 55 else 4 if age < 65 else 5 if age < 75 else 6
                st.session_state.xgb_input_df = pd.DataFrame([{
                    'AGECL': int(agecl), 'EDCL': int(edcl), 'MARRIED': int(married), 'KIDS': int(kids),
                    'Knowledge Group': int(knw), 'OCCAT1': int(occ), 'FAMSTRUCT': int(fam), 'HHSEX': int(sex),
                    'ASSET': float(assets), 'INCOME': float(income), 'NETWORTH': float(assets - debt), 
                    'EQUITY': float(assets - debt), 'DEBT': float(debt)
                }])
                st.session_state.client_id = client_id_input
                st.session_state.client_name = client_name_input
                st.session_state.stage = 2
                st.success("Details saved! Proceed to Questionnaire.")

    # --- TAB 2: QUESTIONNAIRE ---
    with tab_questions:
        if st.session_state.stage >= 2:
            st.header("Investment Questionnaire")
            with st.form("q_form"):
                try:
                    df_q = pd.read_csv(os.path.join(os.path.dirname(__file__), 'questions.csv'))

                    ans_list = [st.radio(f"{i}. {r['Question']}", r.iloc[1:].dropna().tolist(), key=f"q_radio_{i}") for i, r in df_q.iterrows()]
                except Exception:
                    st.error("Error: questions.csv file missing.")
                    return

                if st.form_submit_button("Submit and Calculate"):
                    df_w = pd.read_csv(os.path.join(os.path.dirname(__file__), 'weights.csv'))
                    total_w = 0.0
                    for i, ans in enumerate(ans_list):
                        col = df_q.iloc[i][df_q.iloc[i] == ans].index
                        total_w += df_w.loc[i, col].item()
                    
                    st.session_state.total_weight = float(total_w)
                    
                    if loaded_model is not None and st.session_state.xgb_input_df is not None:
                        pred = loaded_model.predict(st.session_state.xgb_input_df)
                        val = int(pred[0]) if isinstance(pred, (np.ndarray, list)) else int(pred)
                        st.session_state.model_risk = {0: 'Conservative', 1: 'Moderate', 2: 'Aggressive'}.get(val, "Unknown")
                    
                    st.session_state.stage = 3
                    st.success("Calculations complete! Proceed to Results.")
        else:
            st.warning("Please complete Personal Information first.")

    # --- TAB 3: RESULTS ---
    with tab_results:
        if st.session_state.stage < 3:
            st.info("Complete Tab 1 and 2 to view assessment.")
        else:
            col_sub, col_ai = st.columns(2)
            
            with col_sub:
                st.subheader("📋 Subjective Assessment")
                tw = st.session_state.total_weight
                if 7 <= tw <= 22:
                    res, lbs, vls, clrs = 'Conservative', ['Bonds'], [100.0], ['darkgoldenrod']
                elif 22 < tw <= 35:
                    res, lbs, vls, clrs = 'Conservative', ['Bonds', 'Cash'], [80.0, 20.0], ['darkgoldenrod', 'silver']
                elif 35 < tw <= 48:
                    res, lbs, vls, clrs = 'Moderate', ['Bonds', 'Stocks'], [60.0, 40.0], ['darkgoldenrod', 'teal']
                else:
                    res, lbs, vls, clrs = 'Aggressive', ['Stocks'], [100.0], ['teal']
                
                st.metric("Subjective Risk", res)
                fig_sub = px.pie(values=vls, names=lbs, color_discrete_sequence=clrs, hole=0.4)
                # assign unique key to questionnaire calculated pie chart
                st.plotly_chart(fig_sub, use_container_width=True, key="subjective_chart_pie")

            with col_ai:
                st.subheader("🤖 AI Recommendation")
                if st.session_state.model_risk:
                    ai_r = st.session_state.model_risk
                    if ai_r == 'Conservative':
                        al, av, ac = ['Bonds', 'Cash'], [80.0, 20.0], ['darkgoldenrod', 'silver']
                    elif ai_r == 'Moderate':
                        al, av, ac = ['Bonds', 'Stocks'], [60.0, 40.0], ['darkgoldenrod', 'teal']
                    else:
                        al, av, ac = ['Stocks'], [100.0], ['teal']
                    
                    st.metric("Objective Profile", ai_r)
                    fig_ai = px.pie(values=av, names=al, color_discrete_sequence=ac, hole=0.4)
                    # assign key to pie chart
                    st.plotly_chart(fig_ai, use_container_width=True, key="ai_chart_pie")
                else:
                    st.error("AI Prediction unavailable.")

            st.divider()
            if st.button("Save Results to Database"):
                f_path = 'client_recommendations.csv'
                f_exists = os.path.isfile(f_path)
                with open(f_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not f_exists:
                        writer.writerow(['Timestamp', 'ClientID', 'ClientName', 'Score', 'SubRisk', 'AIRisk'])
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        st.session_state.client_id,
                        st.session_state.client_name,
                        st.session_state.total_weight,
                        res,
                        st.session_state.model_risk
                    ])
                st.success(f"Record for {st.session_state.client_name} saved!")

if __name__ == "__main__":
    Main_App()
