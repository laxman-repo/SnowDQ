import streamlit as st
import pandas as pd
from pages.Expectations import *
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from pandas import json_normalize
from utils import *
from statistics import mean
from streamlit_modal import Modal
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="SnowDQ", page_icon="static/favicon.ico", layout="wide", initial_sidebar_state="collapsed")
navWithLogo()
# col1, col2 = st.columns((1,8))
# with col1:
#     pass
#     st.image('static/SnowDQ-LOGO.png')
# with col2:
#     page_selected = option_menu(
#             menu_title = None,
#             options = ['Projects', 'Suites', 'Expectations','Datasets'],
#             default_index = 0,
#             icons=['stack','bounding-box','file-earmark-text','folder2'],
#             menu_icon=None,
#             orientation='horizontal',
#             styles={
#             "container": {"padding": "0!important", "background-color": "#fafafa"},
#             # "icon": {"color": "orange", "font-size": "25px"},
#             "icon":{"display":"inline-block"},
#             "nav": {"background-color":"#f2f5f9"},
#             "nav-link": {"font-size": "15px",
#             "font-weight":"bold",
#             "color":"#1d4077",
#             "border-right":"0px solid #1d4077",
#             "border-left":"0px solid #1d4077",
#             "border-top":"0px solid #1d4077",
#             "border-bottom":"0px solid #1d4077",
#             "padding":" 10px",
#             "text-transform": "uppercase",
#             "border-radius":"5px",
#             "margin":"5px",
#             "--hover-color": "#e1e1e1"},
#             "nav-link-selected": {"background-color":"#1d4077", "color":"#ffffff"},
#             }
# )

# st.set_page_config(page_title="SnowDQ | Home", page_icon="static/favicon.ico", layout="wide")
projectsDf = load_data(st.secrets.DQ_TABLE.PROJECT)
projectsDf['MODIFIED_DATE'] = pd.to_datetime(projectsDf['MODIFIED_DATE'])
projectsDf = projectsDf.sort_values(by='MODIFIED_DATE', ascending=False)
dashboardDf = load_data(st.secrets.DQ_TABLE.VALIDATION_RESULTS)
distinctProject = projectsDf.drop_duplicates(subset='NAME')
 
col1,col2 = st.columns((2,8))
with col1:
    st.divider()
    cola,colb = st.columns((8,2))
    with cola:
        search = st.text_input("Search Project",label_visibility="visible", placeholder="Search Project...")
    with colb:
        buttons()
        createProject = st.button("\+", use_container_width=True)
        if "createProject" not in st.session_state:
                st.session_state["createProject"] = False
        if createProject:
                st.session_state["createProject"] = not st.session_state["createProject"]
        if st.session_state["createProject"]:
            createProjectcontainer()
            

    if search:
        df = distinctProject[distinctProject['NAME'].str.contains(search, case=False)]
        selected_row = st.radio("Select a Project:", df['NAME'])

    else:
        cola1, colb2 = st.columns((8,2))
        with cola1:
            selected_row = st.radio("Select a Project:", distinctProject['NAME'])
            print("selected", selected_row)
        with colb2:
            optionButton = st.button("⋮", key=selected_row, use_container_width=True)
            modal = Modal(key="Demo Key", title=" ")
            displayDf = projectsDf[projectsDf["NAME"] == selected_row]   #TODO check for search functionality
            if "optionButton" not in st.session_state:
                st.session_state["optionButton"] = False
            if optionButton:
                st.session_state["optionButton"] = not st.session_state["optionButton"]
            
            if st.session_state["optionButton"]:
                projectId = displayDf['ID'].to_string(index=False)
                print("id>>>>>>>>>>", projectId)
                optionContainer(optionButton, selected_row, projectId)


with col2:
    st.divider()
    if selected_row:
        vr = dashboardDf[dashboardDf['PROJECT_NAME'] == selected_row]
        dq_score= sum(vr['RESULT'].apply(lambda x: json.loads(x).get('success_percentage',0)))
        if dq_score == 0:
            dq_score = 0
        else:
            dq_score = round(dq_score/len(vr['RESULT'].apply(lambda x: json.loads(x).get('success_percentage',0))),2)
        total = sum(vr['RESULT'].apply(calculate_total))
        failed = sum(vr['RESULT'].apply(calculate_unexpected))
        passed = total -failed
        st.write(f"<h1>{displayDf['NAME'].to_string(index=False)}</h1>", unsafe_allow_html=True)
        st.write(f"<h4>{displayDf['DESCRIPTION'].to_string(index=False)}</h4>", unsafe_allow_html=True)
        project_dashboard(dqScore=dq_score, total=total, failed=failed, success=passed)
        st.divider()
        st.dataframe(vr, use_container_width=True,hide_index=True, height=360)
        st.divider()
    else:
        project_dashboard(dqScore=0, total=0, failed=0, success=0)
        st.divider()