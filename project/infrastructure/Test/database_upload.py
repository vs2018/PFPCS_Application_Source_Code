from database import *

# Pandas library used for creating a DataFrame, URL: https://pandas.pydata.org/pandas-docs/stable/
import pandas as pd

db = DatabaseModel()
db.save_master()
# print(db.get_master())

# Source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
df = pd.read_csv("master_data_file.csv")
# Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
df = df.to_dict("records")

DatabaseModel().save(df, "granular", "master")

# Source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
df1 = pd.read_csv("supermarket_prices.csv")


DatabaseModel().save(df1.to_dict("records"), "aggregate", "supermarket")


# Source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
df1 = pd.read_csv("overall_prices.csv")


DatabaseModel().save(df1.to_dict("records"), "aggregate", "non_supermarket")
