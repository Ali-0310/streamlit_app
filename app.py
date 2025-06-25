import streamlit as st
import pandas as pd
import duckdb as db

st.title("Hello from streamlit-app!")
data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9],
}

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Bird"])
with tab1:
    df = pd.DataFrame(data)
    query = st.text_area("Entrez votre requête SQL")
    try:
        result = db.query(query)
        st.dataframe(result)
    except Exception as e:
        st.error(f"Erreur SQL: {e}")

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with tab3:
    st.header("A bird")
    st.image("https://static.streamlit.io/examples/owl.jpg")






