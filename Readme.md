##SnowDQ##
To run app create a file at ".streamlit/secrets.toml".


secrets.toml should contain your snowflake account details in this format.
[connections.snowpark]
account = "account_url"
user = "user_name"
password = "password"
role = "user_role"
warehouse = "warehouse_name"
database = "database_name"
schema = "schema_name"
client_session_keep_alive = true

[DQ_TABLE]
EXPECTATIONS = "SNOWDQ_DB.PUBLIC.DQ_RULES"
SUITE = "SNOWDQ_DB.PUBLIC.DQ_GROUP"
VALIDATION_RESULTS = "SNOWDQ_DB.PUBLIC.DQ_VALIDATION_RESULTS"
PROJECT = "SNOWDQ_DB.PUBLIC.DQ_PROJECT"
SUITE_RULE = "SNOWDQ_DB.PUBLIC.DQ_GROUP_RULE"

[Command to install required packages:]
pip install -r requirements.txt

[Command to run app:]
steamlit run main.py
