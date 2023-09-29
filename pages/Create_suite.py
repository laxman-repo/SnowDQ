## importing the required modules 

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import json


from snowflake_client import *
from utils import *

expectationsDf = load_data(st.secrets.DQ_TABLE.EXPECTATIONS)
items_per_page = 10
st.session_state.page =1

col1,col2,col3=st.columns(3)
with col1:
  suitename= st.text_input("**Suite Name**",placeholder="Enter Suite name...")
with col2:
  description=st.text_input("**Description**", placeholder="Enter Description...")
with col3:
  tags= st.text_input("**Tags**",placeholder="Enter Tags...")

sess = None

st.write("\n")
st.write("\n\n")
with st.container():
    st.markdown("<div style='max-height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
    cola,colb=st.columns([4,9])
    with cola:
        search = st.text_input("Search expectations",placeholder="Search Expectations by name")
        if search:
            page_data = expectationsDf[expectationsDf['RULE'].str.contains(search, case=False)]
        else:
            page_data =expectationsDf
        count=0
        selected_rules_counter=0
        for index, row in page_data.iterrows():
            count += 1
            col3,col4 = st.columns([5,1])
            with col3:
                st.write(page_data['RULE'][index])
            with col4:
                func= st.button('\+', key=f"button_{count}") 
                if 'selected_rules' not in st.session_state:  
                    st.session_state.selected_rules = []
                if func:  # on click button append rule to list 
                    rule = page_data['RULE'][index]
                    st.session_state.selected_rules.append(rule)






with colb:
    st.write("\n")
    addRuleDf = expectationsDf[expectationsDf['RULE'].isin(st.session_state.selected_rules)]
    addRuleDf['ARGS'] = addRuleDf['ARGS'].apply(lambda x: json.loads(x))
    print("---------------",addRuleDf)
    expectation_data = []
    for index, row in addRuleDf.iterrows():
        key = f"{index}_{row['RULE']}"
        st.write("\n---")
        col1, col2,col3 = st.columns([0.1,1, 0.1])
        with col1:
            if row['RULE'] in st.session_state.selected_rules:
                selected_rules_counter += 1  # Increment the counter for each selected rule
                st.write(f"{selected_rules_counter}.")
            
        with col2:
            if row['RULE'] in st.session_state.selected_rules:
                st.write(f"{row['RULE']}")
                rule_dict = {"rule": row['RULE'],
                                "args": {}}
                for i in row['ARGS']:
                    if i['mandatory'].lower() == "yes":
                        name = i['name']
                        st.write(name) 
                        rule_dict["args"][name] = st.text_input("", key = f"{key}_{name}")
        expectation_data.append(rule_dict)


    with col3:
        close_button = st.button(label="X", key=f"close_{index}", on_click=lambda idx=index: remove_rule(idx))
    if close_button:
        st.session_state.st.session_state.selected_rules.remove(row['RULE'])


          


if st.button("save"):
    print("expectation_data",expectation_data)
    # str_json = json.dumps(expectation_data["ARGS"])
    issuite = create_suite(suitename, description, tags)
    
    groupId = issuite[0].ID
    add_rules(groupId, expectation_data)
    st.success("Successfully Created Suite")
    st.cache_data.clear()
    switch_page('Suites')


def remove_rule(index):  
    rule_to_remove = addRuleDf.loc[index, 'RULE']
    st.session_state.selected_rules.remove(rule_to_remove)