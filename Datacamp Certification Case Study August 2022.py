#!/usr/bin/env python
# coding: utf-8

# As part of Datacamp Data Analyst certifiction process I completed and presented my analysis.
# Case study involves analysis of a dataset of fictional website 'Nearly New Nautical'. The marketing team requested insight into what drives page views of advertised second-hand boats which are for sale. More specifically they would like to now if more expensive boats generate higher levels of page views and if there are other features which are common amongst the top-viewed listings, as well as any other relevant marketing trends. 

# **Import libraries and adjust settings:

# In[60]:


import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]=7,7
import seaborn as sns
import numpy as np
pd.set_option('display.max_rows', 5)
pd.set_option('precision', 3)


# **Basic EDA:**
# 
# **Import data file

# In[2]:


df = pd.read_csv(r"C:\Users\User\Downloads\boat_data.csv")


# **Check shape(rows/columns) of df:

# In[3]:


df.shape


# **Explore datatypes of columns:

# In[4]:


df.info()


# **Inspect first few rows of df:

# In[5]:


df.head(5)


# **Check for missing/blank values by column:

# In[6]:


df.isna().sum()


# **Exolore summary statistics for numeric columns:

# In[7]:


df[["Number of views last 7 days","Width","Length"]].describe()


# **Visualise numeric columns to identify outliers:

# In[8]:


fig,ax = plt.subplots(1,3)
sns.boxplot(y="Number of views last 7 days",data=df,ax=ax[0])
sns.boxplot(y="Width",data=df,ax=ax[1])
sns.boxplot(y="Length",data=df,ax=ax[2])
plt.show()


# **Explore non-numeric columns('Type', 'Manufacturer', 'Year Built', 'Location', 'Material' with value counts of 10 most common values:

# In[9]:


df["Type"].value_counts().head(10)


# In[10]:


df["Manufacturer"].value_counts().head(10)


# In[11]:


df["Year Built"].value_counts().head(10)


# In[12]:


df["Material"].value_counts().head(10)


# In[13]:


df["Location"].value_counts().head(10)


# In[14]:


df["Boat Type"].value_counts().head(10)


# In[15]:


df["Type"].value_counts().head(10)


# **Cleaning data:**
# 
# 1)Convert local currencies into UK Pound Sterling(at August 2022 exchange rates)
# 
# 2)Replace the missing data in 'Length' and 'Width' axis with median values.
# 
# 3)Replace NAN with "Unknown" in "Manufacturer","Location" and "Material" axis.**

# In[16]:


df["Currency"] = df["Price"].str[:3]
df["Price strip"] = df["Price"].str.replace(r"[Â£a-zA-Z]",'')
df["Currency"] = df["Currency"].astype("category")
df["Price strip"] = df["Price strip"].astype(int)
exchange_rate = {"CHF":0.86,"EUR":0.84,"DKK":0.11}
df["Currency rate"] = df["Currency"].map(exchange_rate)
df["Currency rate"] = df["Currency rate"].fillna(1)
df["Currency rate"] = df["Currency rate"].astype(float)
df["Price modified"] = df["Currency rate"] * df["Price strip"]
df["Price modified"] = df["Price modified"].astype(int)


# Check summary statistics for 'Price Modified' column:

# In[17]:


df["Price modified"].describe().apply("{0:.1f}".format)


# **Visualise 'Price Modified' column:

# In[18]:


sns.boxplot(y='Price modified',data=df)
plt.show()


# **Use median values in 'Length' and 'Width' to replace missing data:

# In[19]:


median_length = df["Length"].median()
median_width = df["Width"].median()
df["Length"] = df["Length"].fillna(median_length)
df["Width"] = df["Width"].fillna(median_width)


# **Use "Unknown" for missing data in 'Manufacturer','Material','Location'.

# In[20]:


df["Manufacturer"] =df["Manufacturer"].fillna("Unknown")
df["Material"] = df["Material"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")


# **Data transformation:**
# 
# 'Year Built' axis can be used to create 'Age' axis. Where 'Year' is recorded as 0, the median age for new and used boats can be used as a replacement value.

# In[21]:


df["Age"] = 2022 - df["Year Built"]
new_boat_median = df.loc[(df["Age"] < 2022) & (df["Type"].str.contains("new")),"Age"].median()
used_boat_median = df.loc[(df["Age"] < 2022) & (df["Type"].str.contains("Used boat")),"Age"].median()
df["Age"] = np.where((df["Year Built"] == 0) & (df["Type"].str.contains("new")),new_boat_median,df["Age"])
df["Age"] = df["Age"].replace(2022,used_boat_median)


# **Check summary statistics for 'Age' column:

# In[22]:


df["Age"].describe()


# **Visualise 'Age' column:

# In[23]:


sns.boxplot(y="Age",data=df)
plt.show()


# **'Number of view last 7 days','Price modified' and 'Age' axis all show number of outlier values beyond standard IQR *2 + 75th percentile:
# New dataframe created to filter out records with outliers in these columns.
# 
# 

# In[24]:


views_IQR = np.quantile(df["Number of views last 7 days"],.75) - np.quantile(df["Number of views last 7 days"],.25)
views_upper = (views_IQR *1.5) + np.quantile(df["Number of views last 7 days"],.75)


# In[25]:


price_IQR = np.quantile(df["Price modified"],.75) - np.quantile(df["Price modified"],.25)
price_upper = (price_IQR *1.5) + np.quantile(df["Price modified"],.75)


# In[26]:


age_IQR = np.quantile(df["Age"],.75) - np.quantile(df["Age"],.25)
age_upper = (age_IQR *1.5) + np.quantile(df["Age"],.75)


# In[27]:


df_filtered = df[(df["Number of views last 7 days"] < views_upper) & (df["Price modified"] < price_upper) & (df["Age"] < age_upper)]


# In[66]:


df_filtered.shape


# **Relationship between 'Price modified' and 'Number of views last 7 days' explored through scatterplot and correlation:

# In[62]:


sns.scatterplot(x="Price modified",y="Number of views last 7 days",data=df_filtered,alpha=0.1)
plt.show()


# In[29]:


df_filtered["Price modified"].corr(df_filtered["Number of views last 7 days"])


# **Relationship between 'Age' and 'Number of views last 7 days' explored through scatterplot and correlation:

# In[30]:


sns.scatterplot(x="Age",y="Number of views last 7 days",data=df_filtered,alpha=0.2)
plt.show()


# In[31]:


df_filtered["Age"].corr(df_filtered["Number of views last 7 days"])


# **Created a new/used categorial variable for new and other boat type:

# **Visualise page views by new categorical grouping:

# **Groupby new categorial variable and calculate summary statistics:

# **Calculate new categorial groupings to summarise 'Boat Type', 'Material', 'Location', 'Manufacturer' to visualise page views by different categories:

# In[32]:


boat_type_mapping = {"Motor Yacht":"Motor Yacht","Sport Boat":"Sport Boat","Flybridge":"Flybridge","Trawler":"Trawler","Pilothouse":"Pilothouse","Cabin Boat":"Cabin Boat","Hardtop":"Hardtop","Centre console boat":"Centre console boat"}


# In[59]:


df["Boat Type"].map(boat_type_mapping)


# In[63]:


ax = sns.stripplot(x="Boat Type - agg",y="Number of views last 7 days",data=df_filtered,jitter=0.35)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
plt.show()


# In[35]:


df_filtered.groupby("Boat Type - agg")["Number of views last 7 days"].agg([np.median,np.mean,max,min,np.std])


# In[36]:


material_mapping = {"GRP":"GRP","PVC":"PVC","Steel":"Steel","Wood":"Wood","Aluminium":"Aluminium"}


# In[55]:


df_filtered["Material"].map(material_mapping)


# In[38]:


ax = sns.stripplot(x="Material - agg",y="Number of views last 7 days",data=df_filtered,jitter=0.35)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
plt.show()


# In[39]:


df_filtered.groupby("Material - agg")["Number of views last 7 days"].agg([np.median,np.mean,max,min,np.std])


# In[40]:


location_mapping = {"Germany":"Germany","Italy":"Italy","France":"France","Netherlands":"Netherlands","Switzerland":"Switzerland","Croatia":"Croatia","Spain":"Spain","United":"United Kingdom"}


# In[52]:


df_filtered["Location"].map(location_mapping)


# In[65]:


ax = sns.stripplot(x="Location - agg",y="Number of views last 7 days",data=df_filtered,jitter=0.35)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
plt.show()


# In[43]:


df_filtered.groupby("Location - agg")["Number of views last 7 days"].agg([np.median,np.mean,max,min,np.std])


# In[ ]:





# In[44]:


manufacturer_mapping = {"BÃ©nÃ©teau power boats":"BÃ©nÃ©teau","Jeanneau power boats":"Jeanneau","Sea Ray power boats":"Sea Ray","Sunseeker power boats":"Sunseek","Cranchi power boats":"Cranchi","Bavaria power boats":"Bavaria","Quicksilver (Brunswick Marine) power boats":"Quicksilver-Brunswick Marine"}


# In[53]:


df_filtered["Manufacturer"].map(manufacturer_mapping)


# In[64]:


ax = sns.stripplot(x="Manufacturer - agg",y="Number of views last 7 days",data=df_filtered,jitter=0.30)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 30)
plt.show()


# In[47]:


df_filtered.groupby("Manufacturer - agg")["Number of views last 7 days"].agg([np.median,np.mean,max,min,np.std])


# **Check for relationship between views and length/width:

# In[48]:


sns.scatterplot(x="Width",y="Number of views last 7 days",data=df_filtered)
plt.show()


# In[49]:


df_filtered["Number of views last 7 days"].corr(df_filtered["Width"])


# In[50]:


sns.scatterplot(x="Length",y="Number of views last 7 days",data=df_filtered)
plt.show()


# In[51]:


df_filtered["Number of views last 7 days"].corr(df_filtered["Length"])


# In[ ]:


df

