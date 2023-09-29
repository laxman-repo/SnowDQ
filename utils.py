import pandas as pd
import streamlit as st
import json
from streamlit_modal import Modal
from streamlit_extras.stylable_container import stylable_container
from snowflake_client import *
from streamlit_extras.switch_page_button import switch_page


def paginate_dataframe(df, page_number, page_size):
    """
    Paginate a Pandas DataFrame and return the specified page.

    Args:
        df (pd.DataFrame): The DataFrame to paginate.
        page_number (int): The page number to retrieve (1-based index).
        page_size (int): The number of rows per page.

    Returns:
        pd.DataFrame: The specified page of the DataFrame.
        int: Total number of pages.
    """
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size  # Calculate total pages

    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size

    return df.iloc[start_idx:end_idx], total_pages

"""
Example usage:
page_number = 2  # Display the second page
page_size = 10  # 10 rows per page
page_data, total_pages = paginate_dataframe(df, page_number, page_size)
"""



def success(txt):
    # txt="Production"    
    htmlstr1=f"""<p style='background-color:#c7e9cc;
    color:#1fa531;
    font-size:14px;
    border-radius:30px;
    line-height:40px;
    padding-left:22px;
    opacity:0.6'>
    {txt}</style>
    <br></p>"""
    st.markdown(htmlstr1,unsafe_allow_html=True)
    
def suite_owner_circle(text):
    circle_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Define the styles for the circle */
            .circle {{
                width: 40px;
                height: 40px;
                background-color: #e6ecf3;
                border-radius: 50%;
                text-align: center;
                line-height: 40px;
                color: #08101c;
                font-size: 24px;
            }}
        </style>
    </head>
    <body>
        <!-- Create the circle and add text inside it -->
        <div class="circle">{text}</div>
    </body>
    </html>
    """
    st.markdown(circle_html,unsafe_allow_html=True)

def suite_rule_background(text):
    suite_rule_background = f"""
    <!DOCTYPE html>
<html>
<head>
    <style>
        /* Define the styles for the background */
        .background {{
            display: inline-block;
            background-color: #e6ecf3; /* Background color */
            padding: 10px; /* Padding to create space around the text */
            border-radius: 30px; /* Rounded corners */
            color: #08101c; /* Text color */
            font-size: 18px; /* Font size */
        }}
    </style>
</head>
<body>
    <!-- Create the text with a background -->
    <div class="background">{text}</div>
</body>
</html>
    """
    st.markdown(suite_rule_background,unsafe_allow_html=True)





def html(df_dot,index):
    with stylable_container(
                    key="container_with_border",
                    css_styles="""
                        {
                            z-index:9999999;
                            background-color: #AED6F1 ;
                            position: fixed;
                            top: 1%;
                            right: 0;
                            width: 800px;
                            height: 100%;
                            border  : 3px solid blue;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            border-radius: 0.5rem;
                            padding: calc(1em - 1px)
                        }
                        """,
                ):
        with st.container():
            d = index
            st.write("**Expectation Details**")
            st.markdown("---")
            rule = df_dot['RULE'][d]
            st.write(f"**{rule}**")
            st.markdown('---')
            st.write("**Description**")
            st.write(df_dot['DESCRIPTION'][d])
            st.markdown('---')
            st.write("**Tags**")
            st.write(df_dot["TAGS"][d])
            st.markdown('---')
            st.write("**Backend support**")
            st.write(df_dot["SUPPORTED_BACKEND"][d])
            st.markdown('---')
            buttons()
            if st.button('cancel', key = f"cancel_button_{d}"):
                st.session_state['button']  = False
                st.experimental_rerun()



def buttons():
    button_style = """
    <style>
        .stButton>button {
            margin: 11px; /* Add a 5-pixel margin around the element */
            background-color: #e6ecf3;
            color: #08101c;
            border-radius: 5px;
            padding: 7px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #021859;
            color: #e6ecf3;
            transform: translate(0px, -3px);
        }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)


def project_dashboard(dqScore=0, total=0, failed=0, success=0):
    html_code = f"""
    <style>
    /* Define the CSS for the boxes and container */
    .container {{
        display: flex;
        justify-content: space-between;
    }}
    .box {{
        background-color: #e6ecf3;
        width: 200px; /* Adjust the width as needed */
        height: 120px;
        padding: 20px;
        margin: 15px;
        border-radius: 15px;
    }}
    </style>
    <div class="container">
        <div class="box">
            <p>Average DQ Score</p>
            <p style="font-size: 24px;">{dqScore}</p>
        </div>
        <div class="box">
            <p>Total Records</p>
            <p style="font-size: 24px;">{total}</p>
        </div>
        <div class="box">
            <p>Failed</p>
            <p style="font-size: 24px; color: red;">{failed}</p>
        </div>
        <div class="box">
            <p>Success</p>
            <p style="font-size: 24px; color: green;">{success}</p>
        </div>
    </div>
    """

    st.markdown(html_code, unsafe_allow_html=True)




def calculate_total(result_json):
    # Initialize a variable to store the total
    total = 0
    # Convert the 'result_json' column value to a list of dictionaries
    result_list = json.loads(result_json).get('result_json', [])
    # Iterate through the list and calculate the total
    for item in result_list:
        result = item.get('result', {})
        total += result.get('element_count', 0)
    return total /len(result_list)


def calculate_unexpected(result_json):
    # Initialize a variable to store the total
    total = 0
    # Convert the 'result_json' column value to a list of dictionaries
    result_list = json.loads(result_json).get('result_json', [])
    # Iterate through the list and calculate the total
    for item in result_list:
        result = item.get('result', {})
        total += result.get('unexpected_count', 0)
    return total /len(result_list)

def navWithLogo():
    col1, col2, col3 = st.columns((4,2,4))
    with col2:
        st.image('static/SnowDQ-LOGO.png', use_column_width=True)
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    html_code = """
    <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #e6ecf3; border-radius: 10px; width: 100%;">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav mx-auto">
                <a class="nav-item nav-link" href="/" target="_self">Home</a>
                <a class="nav-item nav-link" href="/Expectations" target="_self">Expectation</a>
                <a class="nav-item nav-link" href="/Suites" target="_self">Suites</a>
            </div>
        </div>
    </nav>
</div>

    """
    col1, col2, col3 = st.columns((3,4,3))
    with col2:
        st.markdown(html_code, unsafe_allow_html=True)


def delete_callback(selected_row):
    with stylable_container(key="container_with_border",css_styles="""{z-index:9999999;
                                                                        background-color: #e6ecf3;
                                                                        position: fixed;
                                                                        top: 40%;
                                                                        right: 45%;
                                                                        width: 25%;
                                                                        height: 35%;
                                                                        border: 3px solid blue;
                                                                        border: 1px solid rgba(49, 51, 63, 0.2);
                                                                        border-radius: 0.5rem;
                                                                        padding: calc(1em - 1px)}"""):
        with st.container():
            st.subheader("**Confirm Delete**")
            st.write("**Are you want to delete a record?**")
            submit_button = st.button("Yes")
            cancel_button = st.button("No")
            if submit_button:
                print("inside submit button with:", selected_row)
                delete_project(selected_row)
                st.session_state["optionButton"] = False
                st.session_state["del_button"] = False
                # st.cache_data.clear()
                st.experimental_rerun()  #TODO Need to find alternate solution
            if cancel_button:
                st.session_state["optionButton"] = False
                st.session_state["del_button"] = False
                st.experimental_rerun()
                # st.session_state["optionButton"] = False
                


def optionContainer(optionButton,selected_row, projectId):
    with stylable_container(key="container_with_border",
        css_styles="""{z-index: 9999999;
        background-color: #e6ecf3;
        position: fixed;
        top: 20%;
        right: 65%;
        width: 20%;
        height: 35%;
        border: 3px solid blue;
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: calc(1em - 1px);}"""):
        with st.container():
            edit = st.button("Edit Project", key=f"edit_button_{optionButton}")
            delete = st.button("Delete Project", key=f"delete_button_{optionButton}")
            suite = st.button("Add/Remove Suite", key=f"suite_button_{optionButton}")

            if "edit_button" not in st.session_state:
                st.session_state["edit_button"] = False

            if "del_button" not in st.session_state:
                st.session_state["del_button"] = False

            if "suite_button" not in st.session_state:
                st.session_state["suite_button"] = False

            if edit:
                st.session_state["edit_button"] = not st.session_state["edit_button"]

            if delete:
                st.session_state["del_button"] = not st.session_state["del_button"]

            if suite:
                st.session_state["suite_button"] = not st.session_state["suite_button"]

        if st.session_state["edit_button"] == True:
            # pass
            edit_callback(selected_row)
        if st.session_state["del_button"] == True:
            # pass
            delete_callback(selected_row)
        if st.session_state["suite_button"] == True:
            # pass
            addSuite_callback(selected_row, projectId)


def edit_callback(selected_row):
    with stylable_container(key="container_with_border",
                            css_styles="""{background-color: #e6ecf3;
                            position: fixed;
                            top:50px;
                            right: 0;
                            width: 450px;
                            z-index:9999;
                            height: 100%;
                            border: 3px solid blue;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            border-radius: 0.5rem;
                            padding: calc(1em - 1px)}"""):
        with st.container():
            form = st.form(key="my_form")
            form.write("")
            form.write("")
            form.write("**Update Project**")
            name = form.text_input(label="Enter Project Name", value=selected_row, disabled=True )
            # disabled: bool = False,
            form.write("Description")
            description = form.text_area(label="Enter Description")
            form.write("")
            form.write("")
            form.write("")
            submit_button = form.form_submit_button("Update")
            cancel_button = form.form_submit_button(label="Cancel")
            if submit_button:
                update_project(selected_row, description)
                # query = f"""UPDATE dq_project SET name = '{name}', description = '{desc}' WHERE ID={l[d]}"""
                st.session_state["optionButton"] = False
                st.session_state["edit_button"] = False
                st.cache_data.clear()  #TODO Need to find alternate solution
                st.experimental_rerun()
            if cancel_button:
                st.session_state["optionButton"] = False
                st.session_state["edit_button"] = False
                st.experimental_rerun()



def addSuite_callback(selected_row, projectId):
    with stylable_container(key="container_with_border",
                            css_styles="""{
                            background-color: #e6ecf3;
                            position: fixed;
                            top:25px;
                            right: 0;
                            width: 750px;
                            z-index:9999;
                            height: 100%;
                            border: 3px solid blue;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            border-radius: 0.5rem;
                            padding: calc(1em - 1px)}"""):
        
        with st.container():
            group_id = []
            added_suites = []
            suitsDf = load_data(st.secrets.DQ_TABLE.SUITE)
            suitsDf['MODIFIED_DATE'] = pd.to_datetime(suitsDf['MODIFIED_DATE'])
            suitsDf = suitsDf.sort_values(by='MODIFIED_DATE', ascending=False)

            if group_id not in st.session_state:
                st.session_state.group_id = []

            if added_suites not in st.session_state:
                st.session_state.added_suites = []
                

            search = st.text_input("Search Expectation",placeholder="Search suite by name")
            if search:
                suitsDf = suitsDf[suitsDf['NAME'].str.contains(search, case=False)]                        
            
            st.subheader("Add/Remove Suites")
            for index, row in suitsDf.iterrows():
                check = st.checkbox(suitsDf["NAME"][index], key=f"check_{index}")
                if check:
                    st.session_state.group_id.append(suitsDf["ID"][index])
                    st.session_state.added_suites.append(suitsDf["NAME"][index])


            st.write(st.session_state.added_suites)
            print("group_id>>>>>>>>>", st.session_state.group_id)
            save = st.button("Save", key=f"save_{1}")
            cancel = st.button("Cancel", key=f"cancel_{2}")

            if save:
                for gid in st.session_state.group_id:
                    add_suite(projectId, gid)
                st.session_state["suite_button"] = False
                st.session_state["optionButton"] = False
                st.experimental_rerun()
            if cancel:
                st.session_state["suite_button"] = False
                st.session_state["optionButton"] = False
                st.experimental_rerun()



def createProjectcontainer():
    with stylable_container(key="container_with_border",
                            css_styles="""{background-color: #e6ecf3;
                            position: fixed;
                            top:50px;
                            right: 0;
                            width: 450px;
                            z-index:9999;
                            height: 100%;
                            border: 3px solid blue;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            border-radius: 0.5rem;
                            padding: calc(1em - 1px)}"""):
        with st.container():
            st.write("**Add New Project**")
            name = st.text_input(label='Enter Project Name',placeholder='Enter Project Name')
            st.write("Description")
            description = st.text_area(label='Enter Description',placeholder='Enter Description')
            st.write("")
            st.write("")
            st.write("")

            submit_button = st.button('Create Project')
            cancel_button = st.button('Cancel')
            if submit_button:
                print("submit")
                create_project(name, description)
                st.cache_data.clear()  #TODO Need to find alternate solution
                st.session_state['createProject']  = False
                st.experimental_rerun()
            if cancel_button:
                st.session_state['createProject']  = False
                st.experimental_rerun()