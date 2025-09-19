# pylint: disable=missing-module-docstring

import duckdb as db
import streamlit as st

# Connect to the database
con = db.connect(database="data/sql_exercises_tables.duckdb", read_only = False)

#-----------------------------------------------------
# Streamlit app
#-----------------------------------------------------

# Title and description
st.title("SRS application - SQL fundamentals")
st.write(
    "This is a simple application that allows you to study SQL fundamentals using spaced repetition."
)

# Sidebar
with st.sidebar:
    theme = st.selectbox(
        "Which chapter do you want to study?",
        [
            "Cross Join",
            "Group by",
            "Case When",
            "Grouping Sets",
            "Filter",
            "Rollup & Cube",
            "Window Functions",
        ],
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"Theme selected is {theme}")
    # Get the exercises list
    exercise = con.execute(f"SELECT * FROM memory_state WHERE Theme = '{theme}'")
    st.write(exercise)

# ANSWER_QUERY = """
# SELECT * 
# FROM beverages
# CROSS JOIN food_items
# """
# answer_df = db.sql(ANSWER_QUERY).df()


query_input = st.text_area(
    label="Saisissez votre requête SQL", value=None, key="user_input_query"
)

# if query_input:
#     user_answer_df = db.sql(query_input).df()
#     st.dataframe(user_answer_df)

#     # Check of Columns number is the same as the answer_df:
#     if len(user_answer_df.columns) != len(answer_df.columns):
#         st.error("The number of columns is not the same as the answer expected")

#     try:
#         user_answer_df = user_answer_df[answer_df.columns]
#         st.dataframe(answer_df.compare(user_answer_df))
#     except KeyError as e:
#         st.warning(f"The column {e} is not in the user answer. It will be ignored.")

#     n_lines_diff = user_answer_df.shape[0] - answer_df.shape[0]
#     if n_lines_diff != 0:
#         st.error(
#             f"Misssing Columns. You have {n_lines_diff} lines difference with the answer expected"
#         )

    # st.dataframe(user_answer_df.equals(answer_df))

## Display tables and solution
# tab1, tab2 = st.tabs(["Tables", "Solution"])
# with tab1:
#     st.subheader("Table: beverages")
#     st.dataframe(beverages)
#     st.subheader("Table: food_items")
#     st.dataframe(food_items)
#     st.subheader("Table wanted:")
#     st.dataframe(answer_df)

# with tab2:
#     st.write(f"The query is: {ANSWER_QUERY}")
