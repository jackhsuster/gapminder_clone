import sqlite3
import pandas as pd

file_names = ["ddf--datapoints--gdp_pcap--by--country--time",
              "ddf--datapoints--lex--by--country--time",
              "ddf--datapoints--pop--by--country--time",
              "ddf--entities--geo--country"]
table_names =["gdp_per_capita","life_expectancy","population","geography"]
df_dict = dict()
for file_name, table_name in zip(file_names, table_names):
    file_path = f"data/{file_name}.csv"
    df = pd.read_csv(file_path)
    df_dict[table_name] = df
# print(len(df_dict))

con = sqlite3.connect("data/gapminder.db")
for k, v in df_dict.items():
    v.to_sql(name = k,con = con ,index =False , if_exists="replace")

# remove the TABLE if it exists
drop_view_sql = """
DROP VIEW IF EXISTS plotting;
"""
# create the VIEW  plotting JOIN 4 tables
create_view_sql = """
CREATE VIEW plotting AS
SELECT geography.name AS country_name,
       geography.world_4region AS continent,
       gdp_per_capita.time AS dt_year,
       gdp_per_capita.gdp_pcap AS gdp_per_capita,
       life_expectancy.lex AS life_expectancy,
       population.pop AS population
    FROM gdp_per_capita
    JOIN geography
      ON gdp_per_capita.country = geography.country
    JOIN life_expectancy
      ON gdp_per_capita.country = life_expectancy.country AND 
         gdp_per_capita.time = life_expectancy.time
    JOIN population
      ON gdp_per_capita.country = population.country AND
         gdp_per_capita.time = population.time
Where gdp_per_capita.time < 2024
"""
# execute the SQL
cur = con.cursor()
cur.execute(drop_view_sql)
cur.execute(create_view_sql)
con.close()





