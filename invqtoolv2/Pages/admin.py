import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Invq Tool",
    page_icon="📈",
    layout = "wide"
)

##setup main container within the page
admin_container = st.container(border=True, width= 'stretch')
admin_container.title("View csv files")

with admin_container:
    #get file path of questions.csv
    question_upload_path = st.file_uploader("Upload question file (questions.csv) for viewing.") ## load csv file widget
    
    #validate filename and upload into a dataframe for viewing
    if question_upload_path is not None:
        question_file_name = question_upload_path.name
        if question_file_name == 'questions.csv':
            df_questions = pd.read_csv(question_upload_path)
            st.session_state["loaded_questions"] = df_questions
            st.dataframe(df_questions, width='stretch') 
            st.info("Loading successful.")
        else:
            st.info("Please upload questions.csv file to correctly view contents.")


    st.divider()#add horizontal divider

    #get file path of weights.csv
    weights_upload_path = st.file_uploader("Upload weights matrix file (weights.csv) for viewing.")
    
    #validate filename and upload into a dataframe for viewing
    if weights_upload_path is not None:
        weights_file_name = weights_upload_path.name
        if weights_file_name == 'weights.csv':
            #load the answer weights into a dataframe.
            df_answer_weights = pd.read_csv('weights.csv')
            st.dataframe(df_answer_weights, width='stretch')
            st.info("Loading successful.")
        else:
            st.info("Please upload weights.csv file to correctly view contents.")


