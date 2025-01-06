import sqlite3
import pandas as pd

con = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql_query("SELECT * FROM plotting", con = con)
con.close()

# print(plotting_df.shape)  #(42330, 6)

year_to_plot =1800 # year_to_plot = 2023

subset_df = plotting_df[plotting_df["dt_year"] == year_to_plot] # 年分切子集
# 子集中取 life_expectancy 做 Y 軸 , gdp_per_capita 做 X 軸
lex = subset_df["life_expectancy"].values
gdp_pcap = subset_df["gdp_per_capita"].values
cont = subset_df["continent"].values

#print (subset_df["continent"].unique()) # ['asia' 'africa' 'europe' 'americas']
color_map = {
    "asia":"r",
    "africa":"g",
    "europe":"b",
    "americas":"c"
    }

# lex , gdp_pcap , cont 分別是 Y 軸 , X 軸 , 顏色
# 這 3 個 ndarray 用for 迴圈一次一次畫出來 
import matplotlib.pyplot as plt

fig, ax = plt.subplots() # 建立畫布 , 軸物件
for xi ,yi ,ci in zip(gdp_pcap,lex,cont):
    ax.scatter(xi,yi , color = color_map[ci])
ax.set_title(f"The World in {year_to_plot}")
ax.set_xlabel("GDP per Capita (in USD)")
ax.set_ylabel("Life Expectancy ")
ax.set_ylim(20,100)  # 設定 Y 軸範圍 20歲到100歲
ax.set_xlim(0,100000) # 設定 X 軸範圍 0 元到 100000元
plt.show()






