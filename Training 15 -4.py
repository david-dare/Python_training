
import numpy as np

import pandas as pd

import DateTime as dt

pd.set_option('float_format', '{:f}'.format)
desired_width=320

pd.set_option('display.width', desired_width)

pd.set_option('display.max_columns',20)

df = pd.read_csv(r"C:\Users\User\Downloads\airlines_final.csv")

print(df.head)

print(type(df))

print(df.info())

print(df.describe())

df["dept_time"] = pd.to_datetime(df["dept_time"],infer_datetime_format=True)

df["year"] = df["dept_time"].dt.strftime("%Y")

df["wait_min"] =df["wait_min"].astype("int")

label_range =[0,60,120,150,np.inf]

labels_name = ["Low","Medium","High","Very High"]

df["wait_time_grouped"] =pd.cut(df["wait_min"],bins=label_range,labels=labels_name)

print(df["wait_time_grouped"].value_counts(normalize=True))

print(df["wait_min"].mean())
print(df["wait_min"].min())
print(df["wait_min"].max())
print(df["wait_min"].quantile(.25))
print(df["wait_min"].quantile(.75))
print(df["wait_min"].median())

print(df["day"].unique())

mappings = {"Tuesday":"Weekday","Friday":"Weekday","Thursday":"Weekday","Wednesday":"Weekday","Saturday":"Weekend","Sunday":"Weekend","Monday":"Weekday"}

df["weekday/weekend"] = df["day"].map(mappings)

print(df["weekday/weekend"].value_counts())

df.drop(columns=["day"],inplace=True)

print(df.columns)

print(df.shape)

print(df["destination"].unique)

df["destination"] =df["destination"].str.lower()

print(df["destination"].unique)

df["boarding_area"] = df["boarding_area"].str.strip("Gates")

print(df["boarding_area"].unique())

print(df["dest_region"].unique())

df["dest_region"] = df["dest_region"].replace("EAST US","East US")
df["dest_region"] = df["dest_region"].replace("middle east","Middle East")
df["dest_region"] = df["dest_region"].replace("eur","Europe")

print(df["dest_region"].unique())

print(df["dest_size"].unique())

df["dest_size"] = df["dest_size"].str.strip()
print(df["dest_size"].unique())

print(df.columns)

string_length = df["airline"].str.len()

df_airline_3 = df[string_length > 11]

print(df_airline_3)

weekend = df["weekday/weekend"] == "Weekend"

df_weekend = df[weekend]

print(df_weekend.head())

df_weekend = df_weekend.drop(columns=["weekday/weekend"])

print(df_weekend.head())

print(df["cleanliness"].unique())

print(df["safety"].unique())

print(df["satisfaction"].unique())

df["satisfaction"] =df["satisfaction"].str.replace("Somewhat satsified","Somewhat Satisfied")

print(df["satisfaction"].unique())

print(df.isna().sum())

print(df[df["weekday/weekend"].isna()])

df = pd.read_csv(r"C:\Users\User\Downloads\ride_sharing_new.csv",index_col=0)

print(df.head())

print(df.sort_values("station_A_id").head())

print(df.info())

df["duration"] = df["duration"].str.strip("minutes")

df["duration"] = df["duration"].astype("int")

df["user_type"] = df["user_type"].astype("category")

print(df.info())

print(df["duration"].mean().round(2))

df.rename(columns={"bike_id":"Bike_ID","user_type":"User_Type"},inplace=True)

print(df["User_Type"].describe())

print(df.columns)


print(df["user_birth_year"].unique())

df["user_birth_year"] =pd.to_datetime(df["user_birth_year"],infer_datetime_format=True)

print(df.info())

print(df.groupby(["user_gender","User_Type"])["duration"].mean())

df = pd.read_csv(r"C:\Users\User\Downloads\banking_dirty.csv",index_col=0)

print(df.info())

print(df.describe())

print(df.isna().sum())

df["birth_date"]= pd.to_datetime(df["birth_date"],infer_datetime_format=True)
df["account_opened"]= pd.to_datetime(df["account_opened"],infer_datetime_format=True)
df["last_transaction"]= pd.to_datetime(df["last_transaction"],infer_datetime_format=True)

print(df.info())

df["birth_year"] = df["birth_date"].dt.strftime("%Y")

print(df.head())


equiv_amount = df[["fund_A","fund_B","fund_C","fund_D"]].sum(axis=1) == df["inv_amount"]

equiv_df = df[~equiv_amount]

print(equiv_df)

df["year_account_open"] = df["account_opened"].dt.strftime("%Y")

print(df[["account_opened","year_account_open"]].head())


df["acc+inv_amount"] = df[["acct_amount","inv_amount"]].sum(axis=1)

print(df[["acct_amount","inv_amount","acc+inv_amount"]].head())

equal_df = df[df[["acct_amount","inv_amount"]].sum(axis=1) == df["acc+inv_amount"]]

df_dates = df[df["account_opened"] > df["last_transaction"]]

print(df_dates)
print(df_dates.shape)

import DateTime as dt

today = pd.to_datetime("today")

print(today)

df.loc[df["last_transaction"] < df["account_opened"],"last_transaction"] = today

df["last_transaction"]= pd.to_datetime(df["last_transaction"]).dt.date

print(df.head(15))



print(df.columns)

print("mean is",df["acct_amount"].mean().round(1))
print("median is",df["acct_amount"].median().round(1))
print("max is ",df["acct_amount"].max().round(1))
print("min is",df["acct_amount"].min().round(1))
print("1st quantile is",df["acct_amount"].quantile(.25).round(1))
print("3rd quantile is",df["acct_amount"].quantile(.75).round(1))

label_ranges = [0,59218,83344,95097,np.inf]
labels =  ["Low","Medium","High","Very High"]

df["acct_amount_grouped"] =pd.cut(df["acct_amount"],bins=label_ranges,labels=labels)

print(df[["acct_amount","acct_amount_grouped"]])

print(df["acct_amount_grouped"].value_counts(normalize=True))

print(df.groupby("acct_amount_grouped")["acct_amount"].agg(["mean","median","min","max"]).round(2))

new_df = pd.read_csv(r"C:\Users\User\Downloads\banking_dirty.csv",index_col=0)

print(new_df)

df_1 = df.append(new_df,ignore_index=True)

print(df_1.shape)
#duplicates = df.duplicated(subset=["cust_id"],keep=False)

#print(df[~duplicates])

print(df_1.loc[[0,100],])

duplicates = df_1.duplicated(subset="cust_id",keep="first")

df_1 = df_1[duplicates]

print(df_1)
df_1["birth_date"] = pd.to_datetime(df_1["birth_date"],infer_datetime_format=True)

print(df_1)

my_array = np.array(df["acct_amount"])

print(type(my_array))

my_series = pd.Series(my_array)

print(type(my_series))

print((my_series).round(2))

print(my_series.dtype)

print(df.isna().sum())

#df["year_account_open"].replace("2018",np.nan)

print(df.isna().sum())

print(df.head())

df["year_account_open"] = df["year_account_open"].replace("2018",np.nan)

print(df.head())

print(df.isna().sum())

df["year_account_open"] =df["year_account_open"].fillna("2018")

print(df.shape)

df = df.drop_duplicates(subset=["cust_id"])

print(df.shape)

from fuzzywuzzy import process

df = pd.read_csv(r"C:\Users\User\Downloads\restaurants_L2_dirty.csv",index_col=0)

print(df.columns)

print(df.head())
types = df["type"].unique()

print(types)

print(process.extract("italian",types,limit=len(types)))

print(process.extract("american",types,limit=len(types)))

matches = process.extract("italian",df["type"],limit=df.shape[0])

print(matches)

df = pd.read_csv(r"C:\Users\User\Downloads\police.csv")

print(df.head())

df.drop(columns=["county_name","state"],inplace=True)

print(df.shape)

print(df.isna().sum())

df.dropna(subset=["driver_gender"],inplace=True)

print(df.isna().sum())

print(df.info())

df["is_arrested"] = df["is_arrested"].astype("bool")

print(df.info())

df["stop_date_time"] = df["stop_date"].str.cat(df["stop_time"],sep=" ")

df["stop_date_time"] = pd.to_datetime(df["stop_date_time"])

print(df["stop_date_time"].dtype)

df.set_index("stop_date_time",inplace=True)

print(df.index)

print(df["violation"].value_counts(ascending=False))

print(df["violation"].value_counts(ascending=False,normalize=True))

print(df.sort_index(ascending=False))

print(df["search_conducted"].mean())

print(df.groupby(["violation","driver_race"])["search_conducted"].mean())

print(df["is_arrested"].mean())

print(df.groupby(["driver_race","driver_gender"])["is_arrested"].mean())

is_searched =  df[df["search_conducted"] == True]

print(is_searched.shape)

print(df.columns)
print(df["search_conducted"].value_counts())

print(is_searched["search_type"].value_counts(ascending=True,normalize=True))


df["frisk"] = df["search_type"].str.contains("Protective Frisk",na=False)

is_searched["frisk"] = is_searched["search_type"].str.contains("Protective Frisk",na=False)

print(df.columns)

print(df["frisk"].dtype)

print(df["frisk"].mean())

print(df["frisk"].value_counts())

print(df["search_type"].unique())

print(df["frisk"].mean())

print(is_searched["frisk"].mean())

print(df["frisk"].value_counts())

print(is_searched["frisk"].value_counts())

print(pd.crosstab(df["frisk"],df["search_conducted"]))

print(pd.crosstab(is_searched["frisk"],is_searched["search_conducted"]))

print(is_searched.groupby(["driver_race","driver_gender"])["frisk"].mean())

print(df.columns)

print(df["drugs_related_stop"].resample("M").mean())

print(df["is_arrested"].resample("Y").mean())

monthly_arrests = df["is_arrested"].resample("M").mean()

print(monthly_arrests)
print(type(monthly_arrests))

by_hour = df.groupby(df.index.hour)["is_arrested"].mean()


by_year_2 = df["is_arrested"].resample("Y").mean()

print(by_hour)
print(by_year_2)

print(df["district"])

print(df.groupby("district")["is_arrested"].count())

zone_violation = pd.crosstab(df["district"],df["violation"])

print(zone_violation)

print(type(zone_violation))

zone_x = zone_violation.loc["Zone X1":"Zone X4","Registration/plates"]

print(zone_x)

print(df.columns)

print(df["stop_duration"].unique())

mappings = {"0-15 Min":7.5,"16-30 Min":22.5,"30+ Min":45}

df["stop_duration_mins"] = df["stop_duration"].map(mappings)

print(df[["stop_duration_mins","stop_duration"]].head())

duration_by_violation = df.groupby("violation")["stop_duration_mins"].mean()

print(duration_by_violation)

arrest_by_week = df["is_arrested"].resample("Y").mean()

print(arrest_by_week.head())

is_arrested_df = df[df["is_arrested"] == True]

print(is_arrested_df.head())

print(is_arrested_df["stop_duration"].dtype)

order_1 = ["15 Min","16-30 Min","30+ Min"]

df["stop_duration"] = df["stop_duration"].astype("category")

print(df["stop_duration"].dtype)

print(df["stop_duration"].unique())

print(zone_violation)

print(type(zone_violation))

print(zone_violation.loc[:,"Equipment"])

weather_df = pd.read_csv(r"C:\Users\User\Downloads\weather.csv")

print(weather_df.columns)

print(weather_df[["TAVG","TMIN","TMAX"]].describe())

weather_df["diff_max_min"] = weather_df["TMAX"] - weather_df["TMIN"]

weather_df["max > min"] = weather_df["diff_max_min"] > 0

print(weather_df["max > min"].value_counts())

WT = weather_df.loc[:,"WT01":"WT22"]

print(WT.head())
weather_df["total_weather_conditions"] = WT.sum(axis="columns")

print(weather_df["total_weather_conditions"].head())

weather_mapping ={0:"Good",1:"Bad",2:"Very Bad",3:"Terrible",4:"Terrible",5:"Terrible",6:"Terrible",7:"Terrible",8:"Terrible",9:"Terrible"}

weather_df["total_weather_conditions_mapped"] = weather_df["total_weather_conditions"].map(weather_mapping)

print(weather_df[["total_weather_conditions","total_weather_conditions_mapped"]].head())

print(weather_df["total_weather_conditions_mapped"].dtype)

weather_df["total_weather_conditions_mapped"] = weather_df["total_weather_conditions_mapped"].astype("category")

print(weather_df["total_weather_conditions_mapped"].dtype)

print(weather_df["total_weather_conditions_mapped"].unique())

cats =["Good","Bad","Very Bad","Terrible"]

#weather_df["total_weather_conditions_mapped"] = weather_df["total_weather_conditions_mapped"].astype("category", ordered=True, categories=cats,inplace=True)

print(weather_df["total_weather_conditions_mapped"].unique())

print(weather_df.isna().sum())

print(weather_df["total_weather_conditions_mapped"].value_counts())

print(weather_df.index)

df.reset_index(inplace=True)

print(df.index)

print(df.groupby("violation_raw")["stop_duration_mins"].mean().sort_values(ascending=False))



print(df.columns)

total_df = pd.merge(left=df,right=weather_df,left_on="stop_date",right_on="DATE",how="left")

print(total_df.head())

total_df.set_index("stop_date",inplace=True)

final_table = total_df.groupby(["violation","total_weather_conditions_mapped"])["is_arrested"].mean()

print(final_table)

print(type(final_table))

print(total_df.groupby("total_weather_conditions_mapped")["is_arrested"].mean())

#print(final_table["Moving violation","Bad"])

#print(final_table.loc["Equipment":"Moving violation","Bad"])

final_pivot_table = total_df.pivot_table(index="violation",columns="total_weather_conditions_mapped",values="is_arrested")

print(final_pivot_table)

print(total_df["total_weather_conditions_mapped"].dtype)

total_df["total_weather_conditions_mapped"] = total_df["total_weather_conditions"].astype("str")

print(total_df["total_weather_conditions_mapped"].dtype)

cats =["Good","Bad","Very Bad","Terrible"]

total_df["total_weather_conditions_mapped"] = total_df["total_weather_conditions_mapped"].astype("category")

print(total_df["total_weather_conditions_mapped"].unique())


print(total_df["total_weather_conditions_mapped"].head())

print(df.head())

df["year"] = df["stop_date_time"].dt.strftime("%Y")

print(df["year"].head())

df.set_index("stop_date_time",inplace=True)

print(df["is_arrested"].resample("M").count())

print(df.groupby("year")["stop_date"].count())

print(weather_df.columns)

print(weather_df["TAVG"].describe())

label_ranges = [0,30,68,np.inf]

label_names = ["low","medium","high"]

weather_df["temp ranges"] = pd.cut(weather_df["TAVG"],bins=label_ranges,labels=label_names)

print(weather_df[["TAVG","temp ranges"]])

weather_df["temp ranges"].astype("category")

print(weather_df["temp ranges"].value_counts())

print(weather_df["temp ranges"].dtype)

weather_df["temp ranges"] = weather_df["temp ranges"].cat.reorder_categories(new_categories=["high","medium","low"],ordered=True)

print(weather_df["temp ranges"].unique())




