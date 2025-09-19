# pylint: disable=missing-module-docstring

import duckdb as db
import streamlit as st
import ast

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
        "Quel chapitre voulez-vous étudier ?",
        [
            "cross_join",
            "window_functions",
            "Case When",
            "Grouping Sets",
        ],
        index=0,  # Valeur par défaut sélectionnée à chaque synchronisation de la page
        placeholder="Sélectionnez un thème...",
    )
    st.write(f"Theme selected is {theme}")
    # Get the exercises list
    exercise = con.execute(f"SELECT * FROM memory_state WHERE Theme = '{theme}'").df()
    st.dataframe(exercise)

# ANSWER_QUERY = """
# SELECT * 
# FROM beverages
# CROSS JOIN food_items
# """
# answer_df = db.sql(ANSWER_QUERY).df()


query_input = st.text_area(
    label="Saisissez votre requête SQL", value=None, key="user_input_query"
)

if query_input:
    user_query = con.execute(query_input).df()
    st.dataframe(user_query)

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
tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    # Display tables available and table expected
    exercise_tables = ast.literal_eval(exercise.loc[0,"tables"])
    st.subheader("Tables Disponibles:")
    for table in exercise_tables:
        st.subheader(f"{table}")
        st.dataframe(con.execute(f"SELECT * FROM {table}").df())

    st.subheader("Table wanted:")
    ANSWER_STR = exercise.loc[0,"Exercise_name"]
    with open(f'answers/{ANSWER_STR}.sql', 'r') as file:
        answer = file.read()
    st.dataframe(con.execute(answer).df())

# Display the answer query
with tab2:
    st.write(f"The query is: {answer}")
