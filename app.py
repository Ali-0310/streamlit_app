# pylint: disable=missing-module-docstring

import duckdb as db
import streamlit as st
import logging
import os
import pandas as pd

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
# Functions refacored
# -----------------------------------------------------
def check_user_query(user_df: pd.DataFrame, df_expected: pd.DataFrame) -> None:
    """
    Checks if the user's DataFrame matches the expected DataFrame.
    Displays appropriate Streamlit messages for errors, warnings, and success.

    Args:
        user_df (pd.DataFrame): The DataFrame resulting from the user's query.
        df_expected (pd.DataFrame): The expected DataFrame for comparison.
    """
    try:
        # Check if the number of columns is the same
        if len(user_df.columns) != len(df_expected.columns):
            st.error("Le nombre de colonnes n'est pas le même que celui attendu.")

        # Try to reorder the columns as expected
        try:
            user_df = user_df[df_expected.columns]
        except KeyError as e:
            st.warning(
                f"La colonne {e} n'est pas présente dans votre réponse. Elle sera ignorée."
            )
            # Remove missing columns to avoid further errors
            user_df = user_df[
                [col for col in user_df.columns if col in df_expected.columns]
            ]

        n_lines_diff = user_df.shape[0] - df_expected.shape[0]
        if n_lines_diff != 0:
            st.error(
                f"Il y a une différence de {n_lines_diff} lignes avec la réponse attendue."
            )

        try:
            if user_df.equals(df_expected):
                st.dataframe(user_df)
                st.balloons()
                st.success("La réponse est correcte !")
            else:
                st.error("La réponse est incorrecte, veuillez réessayer.")
        except KeyError as e:
            st.error(
                f"Erreur lors de la comparaison des DataFrames : colonne manquante {e}"
            )

    except KeyError as e:
        st.error(f"Erreur inattendue de clé : {e}")


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

# --------------------------------------------------------------------------------------------------
# Get the memory state table
# --------------------------------------------------------------------------------------------------
# Query to get the list of exercises
query_exercises_list = "SELECT * FROM memory_state"
memory_state_df = con.execute(query_exercises_list).df()

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------
with st.sidebar:
    theme = st.selectbox(
        "Quel chapitre voulez-vous étudier ?",
        memory_state_df["theme"].unique(),
        index=None,
        placeholder="Sélectionnez un thème...",
    )
    if theme:
        st.write(f"Thème sélectionné : {theme}")
        query = f"{query_exercises_list} WHERE theme = '{theme}'"
    else:
        query = query_exercises_list

    # Récupérer et afficher la liste des exercices
    exercise = (
        con.execute(query).df().sort_values(by="last_reviewed").reset_index(drop=True)
    )
    st.dataframe(exercise)

# -----------------------------------------------------
# Retrieve the answer query
# -----------------------------------------------------
ANSWER_STR = exercise.loc[0, "exercise_name"]
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

    # Check if the User's query is valid:
    check_user_query(user_answer_df, answer_df)

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
