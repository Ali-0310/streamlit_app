import io
import pandas as pd
import duckdb as db
import os

# Supprimer le fichier de base de données s'il existe
db_file = "data/sql_exercises_tables.duckdb"
if os.path.exists(db_file):
    os.remove(db_file)

# Créer une nouvelle connexion
con = db.connect(database=db_file, read_only=False)

# -----------------------------------------------------
# Exercises List
# -----------------------------------------------------
data = {
    "theme": ["cross_join", "cross_join"],
    "exercise_name": ["beverages_and_food", "tshirt_sales"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
}

memory_state_df = pd.DataFrame(data)
con.execute("DROP TABLE IF EXISTS memory_state")
con.execute("CREATE TABLE memory_state AS SELECT * FROM memory_state_df")


# -----------------------------------------------------
# Cross Join Exercise
# -----------------------------------------------------
# beverages and food items
# -----------------------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

# -----------------------------------------------------
# Tshirt sales
# -----------------------------------------------------
sizes_table = """
sizes
XS
M
L
XL
"""
sizes_df = pd.read_csv(io.StringIO(sizes_table))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes_df")

trademarks_table = """
trademarks
Nike
Asphalt
Abercrombie
Levis
"""
trademarks_df = pd.read_csv(io.StringIO(trademarks_table))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks_df")
