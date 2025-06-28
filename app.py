import streamlit as st
import pandas as pd
import duckdb as db
import io

st.title("SRS application - SQL fundamentals")
st.write("This is a simple application that allows you to study SQL fundamentals using spaced repetition.")

# data 
csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer_query = """
SELECT * 
FROM beverages
CROSS JOIN food_items
"""
answer_df = db.sql(answer_query).df()

with st.sidebar:
    options = st.selectbox(
            "Which chapter do you want to study?",
            ["Joins","Group by","Case When","Grouping Sets","Filter","Rollup & Cube","Window Functions"],
            index = None,
            placeholder = "Select a theme..."
    )
    st.write(f"Theme selected is {options}")

query_input = st.text_area(
    label = "Saisissez votre requête SQL",
    value = None,
    key = "user_input_query"
)
if query_input:
    user_answer_df = db.sql(query_input).df()
    st.dataframe(user_answer_df)

## Display tables and solution
tab1, tab2 = st.tabs(["Tables","Solution"])
with tab1:
    st.subheader("Table: beverages")
    st.dataframe(beverages)
    st.subheader("Table: food_items")
    st.dataframe(food_items)
    st.subheader("Table wanted:")
    st.dataframe(answer_df)

with tab2:
    st.write(f"The query is: {answer_query}")   







