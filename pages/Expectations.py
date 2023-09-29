import streamlit as st
import pandas as pd
import json
from snowflake_client import load_data
from utils import *
from streamlit_extras.switch_page_button import switch_page

# st.set_page_config(page_title="SnowDQ | Expectations", page_icon="static/favicon.ico", layout="wide", initial_sidebar_state="collapsed")
navWithLogo()
expectationsDf = load_data(st.secrets.DQ_TABLE.EXPECTATIONS)

col1,col2 = st.columns((100,10))
with col1:
    search = st.text_input("Search Expectation",label_visibility="visible", placeholder="Search Expectation...")
with col2:
    items_per_page = st.selectbox("Rows Per Page",[10,25,50],label_visibility="visible")
    # if items_per_page ==25 or items_per_page ==50:
    #     st.session_state.page = 1
if 'page' not in st.session_state:
    st.session_state.page = 1

if search:
    df = expectationsDf[expectationsDf['RULE'].str.contains(search, case=False)]
    page_data, total_pages = paginate_dataframe(df, st.session_state.page, items_per_page)
else:
    page_data, total_pages = paginate_dataframe(expectationsDf, st.session_state.page, items_per_page)

for index, row in page_data.iterrows():
    col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1, 1, 3, 4, 1.2,0.5))

    with col1:
        rule = page_data['RULE'][index]
        st.write(f'<span style="font-size:20px">{rule}</span>', unsafe_allow_html=True)
        st.write(page_data['DESCRIPTION'][index])
    
    with col2:
        st.write("Owner")
        # owner_circle(page_data["OWNER"][index][0])
        suite_owner_circle("GX")
    
    with col3:
        st.write("Category")
        category = page_data["CATEGORY"][index]
        st.write(f'<span style="font-size:24px">{category}</span>', unsafe_allow_html=True)
    
    with col4:
        st.write("Tags")
        tags = json.loads(page_data["TAGS"][index])
        if tags:
            c1,c2,c3 = st.columns((4,5,1))
            with c1:
                suite_rule_background(tags[0])
            with c2:
                suite_rule_background(tags[1])
        else:
            pass
            # suite_rule_background("None")

    with col5:
        st.write("Backend support")
        backend_support = json.loads(page_data["SUPPORTED_BACKEND"][index])
        if backend_support:
            c1,c2,c3 = st.columns((2,2,7))
            with c1:
                suite_rule_background(backend_support[0])
            with c2:
                if len(backend_support)>1:
                    suite_rule_background(backend_support[1])
            with c3:
                if len(backend_support)>2:
                    suite_rule_background(f"+{len(backend_support) -2}")
        else:
            pass
            # suite_rule_background("None")
        # suite_rule_background(backend_support)


    with col6:
        st.write("Status")
        status = page_data["STATUS"][index]
        success(status)

    with col7:
        button_label = "⋮"
        click = st.button(button_label, key=f"button_{index}")
        if click:
            html(page_data,index)
    
    st.markdown("""---""") 
col1, col2, col3= st.columns([40,150,40])
buttons()
if col1.button('Previous Page', key='prev_page'):
    if st.session_state.page > 1:
        st.session_state.page -= 1
        st.experimental_rerun()
if col3.button('Next Page', key='next_page'):
    if st.session_state.page < total_pages:
        st.session_state.page += 1
        st.experimental_rerun()

col2.write(f'Page {st.session_state.page}/{total_pages}')

