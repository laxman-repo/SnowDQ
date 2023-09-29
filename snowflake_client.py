import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
import json


# Establish Snowflake session
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.connections.snowpark).create()

session = create_session()

# Load data table
@st.cache_data
def load_data(table_name):
    """
    Load data from snowflake table.

    Args:
        table_name (str): Snowflake table name.
    Returns:
        pd.DataFrame: The Pandas DataFrame.
    """

    # Read in data table
    table = session.table(table_name)
    print("type of table>>>>>>>>>>>", type(table))
    
    # toPandas() results. This will table into 'snowflake.snowpark.table.Table' into 'pandas.core.frame.DataFrame'.
    tableDf = table.toPandas()
    print("type of tabledf>>>>>>>>>", type(tableDf))
    if 'ACTIVE' in tableDf.columns:
        tableDf = tableDf[tableDf["ACTIVE"] == True]
    return tableDf

# ex:
# df = load_data("PETS.PUBLIC.MYTABLE")



def delete_project(project_name, session=session):
    # query = f"""UPDATE {settings.SNOWFLAKE_GROUPS} SET ACTIVE={False} WHERE ID={group_id}"""
    sql_delete_project = f"UPDATE {st.secrets.DQ_TABLE.PROJECT} SET ACTIVE={False} WHERE NAME='{project_name}';"

    # Execute the SQL INSERT statement
    session.sql(sql_delete_project).collect()
    # session.commit()

def update_project(project_name, description, session=session):
    sql_update_project = f"UPDATE {st.secrets.DQ_TABLE.PROJECT} SET DESCRIPTION= '{description}' WHERE NAME= '{project_name}';"
    # Execute the SQL INSERT statement
    session.sql(sql_update_project).collect()
    # session.commit()

def add_suite(project_id, group_id, session=session):
    # query = f"""INSERT INTO {settings.SNOWFLAKE_PROJECTGROUPS} (project_id, group_id) VALUES('{pg["project_id"]}', '{pg["group_id"]}')"""
    sql_add_suite = f"INSERT INTO {st.secrets.DQ_TABLE.PROJECT_SUITE} (PROJECT_ID, GROUP_ID) VALUES('{project_id}', '{group_id}')"
    # Execute the SQL INSERT statement
    session.sql(sql_add_suite).collect()
    # session.commit()

def create_project(name, description, session=session):
    sql_add_project = f"INSERT INTO {st.secrets.DQ_TABLE.PROJECT} (ID, NAME, DESCRIPTION, OWNER, ACTIVE, CREATED_DATE, MODIFIED_DATE) VALUES(DQ_PROJECT_ID_SEQ.NEXTVAL, '{name}', '{description}', 'Admin', '{True}', CURRENT_DATE(), CURRENT_DATE());"
    # Execute the SQL INSERT statement
    print("query",sql_add_project)
    session.sql(sql_add_project).collect()
    # session.commit()

def create_suite(name, description, tags, session=session):
    sql_add_suite = f"""insert into DQ_GROUP(NAME,DESCRIPTION,TAGS,OWNER,ACTIVE,CREATED_DATE,MODIFIED_DATE)
    select '{name}', '{description}',ARRAY_CONSTRUCT('{tags}') ,'Admin', 'True', CURRENT_DATE(), CURRENT_DATE()"""

    # sql_add_suite = f"INSERT INTO {st.secrets.DQ_TABLE.SUITE} (ID, NAME, DESCRIPTION, TAGS, OWNER, ACTIVE, CREATED_DATE, MODIFIED_DATE)\
    #                 VALUES (DQ_GROUP_ID_SEQ.NEXTVAL, '{name}', '{description}', parse_json('{json.dumps(tags_list)}') , 'Admin', '{True}', CURRENT_DATE(), CURRENT_DATE());"
    # Execute the SQL INSERT statement
    session.sql(sql_add_suite).collect()
    data = session.sql(f"SELECT * FROM {st.secrets.DQ_TABLE.SUITE} WHERE NAME = '{name}'").collect()
    return data


def add_rules(gid,rules):
    for r in rules:
        sql_add_rules = f"""insert into {st.secrets.DQ_TABLE.SUITE_RULE}\
            (RULE,ARGS,DESCRIPTION,SEVERITY,GROUP_ID,CREATED_DATE,MODIFIED_DATE)\
            select '{r["rule"]}', TO_VARIANT(PARSE_JSON('{json.dumps(r["args"])}')) , '{r["rule"]}','Medium','{gid}', CURRENT_DATE(), CURRENT_DATE()"""
        session.sql(sql_add_rules).collect()