# pylint: disable=missing-module-docstring

import duckdb as db
import streamlit as st
import logging
import os

# -----------------------------------------------------
# Database connection and initialization
# -----------------------------------------------------
# Check if the database directory exists, create it if not
if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("The database does not exist. Creating it...")
    os.mkdir("data")

# Check if the database file exists, create it if not
if "sql_exercises_tables.duckdb" not in os.listdir("data"):
    logging.error("The file does not exist. Creating it...")
    exec(open("init_db.py").read())
# -----------------------------------------------------
# Connect to the database
# -----------------------------------------------------
con = db.connect(database="data/sql_exercises_tables.duckdb", read_only=False)

# -----------------------------------------------------
# Streamlit app
# -----------------------------------------------------

# -----------------------------------------------------
# Title and description
# -----------------------------------------------------
st.title("SRS application - SQL fundamentals")
st.write(
    "Ceci est une application simple qui vous permet d'étudier les fondamentaux de SQL en utilisant la répétition espacée."
)

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------
with st.sidebar:
    theme = st.selectbox(
        "Quel chapitre voulez-vous étudier ?",
        [
            "cross_join",
            "window_functions",
            "Case When",
            "Grouping Sets",
        ],
        index=None,
        placeholder="Sélectionnez un thème...",
    )
    # Query to get the list of exercises
    query_exercises_list = "SELECT * FROM memory_state"
    if theme:
        st.write(f"Thème sélectionné : {theme}")
        # Retrieve the exercises list
        exercise = (
            con.execute(f"{query_exercises_list} WHERE Theme = '{theme}'")
            .df()
            .sort_values(by="last_reviewed")
            .reset_index(drop=True)
        )
        st.dataframe(exercise)
    else:
        exercise = (
            con.execute(query_exercises_list)
            .df()
            .sort_values(by="last_reviewed")
            .reset_index(drop=True)
        )
        st.dataframe(exercise)

# -----------------------------------------------------
# Retrieve the answer query
# -----------------------------------------------------
ANSWER_STR = exercise.loc[0, "Exercise_name"]
with open(f"answers/{ANSWER_STR}.sql", "r") as file:
    answer_query = file.read()

answer_df = con.execute(answer_query).df()

# -----------------------------------------------------
# User SQL query input
# -----------------------------------------------------
query_input = st.text_area(
    label="Saisissez votre requête SQL", value=None, key="user_input_query"
)

# -----------------------------------------------------
# Analyze the user's answer
# -----------------------------------------------------
if query_input:
    user_answer_df = con.execute(query_input).df()

    # Check of Columns number is the same as the answer_df:
    if len(user_answer_df.columns) != len(answer_df.columns):
        st.error("Le nombre de colonnes n'est pas le même que celui attendu.")

    try:
        user_answer_df = user_answer_df[answer_df.columns]
    except KeyError as e:
        st.warning(
            f"La colonne {e} n'est pas présente dans votre réponse. Elle sera ignorée."
        )

    n_lines_diff = user_answer_df.shape[0] - answer_df.shape[0]
    if n_lines_diff != 0:
        st.error(
            f"Il y a une différence de {n_lines_diff} lignes avec la réponse attendue."
        )

    if user_answer_df.equals(answer_df):
        st.dataframe(user_answer_df)
        st.balloons()
        st.success("La réponse est correcte !")
    else:
        st.error("La réponse est incorrecte, veuillez réessayer.")

# -----------------------------------------------------
# Display available tables and expected solution
# -----------------------------------------------------
tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    # Display available tables and expected table
    exercise_tables = exercise.loc[0, "tables"]
    st.subheader("Tables disponibles :")
    for table in exercise_tables:
        st.write(f"{table}")
        st.dataframe(con.execute(f"SELECT * FROM {table}").df())

    st.subheader("Table attendue :")
    st.dataframe(answer_df)

# -----------------------------------------------------
# Display the answer query
# -----------------------------------------------------
with tab2:
    st.write(f"La requête attendue est : {answer_query}")
