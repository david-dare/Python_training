import numpy as np

import pandas as pd

import DateTime as dt

pd.set_option('float_format', '{:f}'.format)
desired_width=320

pd.set_option('display.width', desired_width)

pd.set_option('display.max_columns',20)

df = pd.read_csv(r"C:\Users\User\Downloads\airlines_final.csv",index_col=0,dtype={"cleanliness":"category","safety":"category","satisfaction":"category"})

print(df.head())

print(df.shape)

print(df.columns)

print(df.info())

print(df["dept_time"].head())

df["dept_time"] = pd.to_datetime(df["dept_time"])

print(df["dept_time"].dtype)

print(df.info())

print(df.describe())

print(df[["dest_region","dest_size","boarding_area","satisfaction"]].describe())

print(df["dest_region"].unique())

mappings = {"EAST US":"East US"}


df["dest_region"] = df["dest_region"].str.replace("EAST US","East US")

print(df["dest_region"].unique())

df["dest_region"] = df["dest_region"].str.replace("eur","Europe")
df["dest_region"] = df["dest_region"].str.replace("middle east","Middle East")

print(df["dest_region"].unique())

print(df["cleanliness"].unique())

print(df["safety"].unique())

print(df["satisfaction"].unique())

df["destination"] = df["destination"].str.lower()

destinations = df["destination"].value_counts(normalize=True)

print(destinations.sort_values(ascending=False))

print(df["wait_min"].mean())

df["boarding_area"] = df["boarding_area"].str.strip("Gates")

print(df["boarding_area"].value_counts(normalize=True))

print(df.isna().sum())

print(df["satisfaction"].value_counts(normalize=True))


print(df.groupby("day")["satisfaction"].value_counts(normalize=True))

print(df["wait_min"].describe())

print(df["wait_min"].dtype)


print(df[["wait_min","wait_min_grouped"]].head())

print(df["day"].head())

print(df["dept_time"].head())

#print(df.resample("M"))

print(df["dept_time"].dtype)

df_monthly = df.set_index("dept_time")

print(df_monthly.index)

print(df_monthly)

df_resample = df_monthly["wait_min"].resample("Y").mean()

print(df_resample)

replacements = {"Asia":"Asian/Oceania"}

df["dest_region"] = df["dest_region"].replace(replacements)


asian_oceania = df.loc[df["dest_region"] == "Asian/Oceania",["day","airline","wait_min"]]

print(asian_oceania.head())

print(df["wait_min"].dtype)

df["wait_min"] = df["wait_min"].astype("str")

print(df["wait_min"].dtype)

df = df.set_index("id")
print(df.index)

print(pd.crosstab(df["airline"],df["dest_region"]))

airlines = df.groupby("airline").count()


filter_list = ["ALASKA","DELTA","UNITED INTL"]

airlines = df[df["airline"].isin(filter_list)]

print(airlines["airline"].unique())

print(airlines)

print(airlines.groupby("airline")["satisfaction"].value_counts(normalize=True))


print(airlines)

df["dept_time"] = pd.to_datetime(df["dept_time"])

df_monthly = df.set_index("dept_time")

df_monthly["wait_min"] = df_monthly["wait_min"].astype(float)

print(df["wait_min"].dtype)

print(df_monthly.index)

print(df_monthly)

print(df_monthly.index.dtype)

print(df_monthly["wait_min"].resample("M").mean())

print(df["dept_time"].min())

print(df.head())

#new_table = pd.pivot_table(index="airline",columns="day",values="wait_min",data=df)

#print(new_table)



df = df.reset_index()

print(df.head())

df = df.drop_duplicates(subset=["id"])

df["wait_min"] = df["wait_min"].astype(float)

grouped_table = df.groupby(["airline","dest_region"])["wait_min"].mean()

print(grouped_table)

print(grouped_table["ALASKA":"CATHAY PACIFIC"])

pivot_table  = pd.pivot_table(index="airline",values="wait_min",columns ="day",data=df,margins=True)

print(pivot_table)

totals = pivot_table.loc[:,"Friday":"Wednesday"]

pivot_table["totals"] = totals.sum(axis="columns")

print(pivot_table["totals"])

print(df.columns)

df["day"] = df["dept_time"].dt.day

print(df["day"].head())

labels= ["low","medium","high","very high"]

range = [0,100,170,190,np.inf]


pivot_table  = pd.pivot_table(index="airline",values="wait_min",columns ="day",data=df,margins=True)

print(pivot_table)

totals = pivot_table.loc[:,"Friday":"Wednesday"]

pivot_table["totals"] = totals.sum(axis="columns")

print(pivot_table["totals"])
