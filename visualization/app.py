import streamlit as st
import pandas as pd
from google.cloud import bigquery
from openai import OpenAI

# CONFIG
PROJECT_ID = "project-f8ec109b-9e2d-4831-899"
TABLE_ID = f"{PROJECT_ID}.event_pipeline.processed_events"

# Initialize clients
bq_client = bigquery.Client()

# 🔑 Set your OpenAI key
OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client = OpenAI(api_key=OPENAI_API_KEY)


# 🧠 Convert natural language → SQL
def generate_sql(user_query: str) -> str:
    prompt = f"""
    You are a data analyst.

    Convert the following question into a BigQuery SQL query.

    Table: {TABLE_ID}

    Schema:
    - event_id (STRING)
    - event_type (STRING)
    - user_id (STRING)
    - amount (FLOAT)
    - timestamp (TIMESTAMP)
    - flagged (BOOLEAN)
    - reason (STRING)

    Rules:
    - Always use LIMIT 100
    - Only use this table
    - Return only SQL (no explanation)

    Question: {user_query}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()



# 📊 Run query
def run_query(sql: str):
    try:
        query_job = bq_client.query(sql)
        return query_job.to_dataframe()
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()


# 🎨 Streamlit UI
st.title("📊 AI-Powered Event Analytics")

user_query = st.text_input("Ask something about your data:")

if st.button("Run Query") and user_query:
    with st.spinner("Generating SQL..."):
        sql = generate_sql(user_query)

    st.code(sql, language="sql")

    with st.spinner("Running query..."):
        df = run_query(sql)

    if not df.empty:
        st.dataframe(df)

        # Auto visualization
        if len(df.columns) >= 2:
            try:
                st.bar_chart(df.set_index(df.columns[0]))
            except:
                pass
