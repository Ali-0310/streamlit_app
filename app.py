import streamlit as st
import pandas as pd
import duckdb as db

st.title("SRS application - SQL fundamentals")
st.subheader("This is a simple application that allows you to study SQL fundamentals using spaced repetition.")

data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9],
}

options = st.selectbox(
    "Which chapter do you want to study?",
    ["Joins","Group by","Case When","Grouping Sets","Filter","Rollup & Cube","Window Functions"],
    index = None,
    placeholder = "Select a theme..."
)

st.write(f"Theme selected is {options}")

df = pd.DataFrame(data)
query = st.text_area("Entrez votre requête SQL")
try:
    result = db.query(query)
    st.dataframe(result)
except Exception as e:
    st.error(f"Erreur SQL: {e}")







