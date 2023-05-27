#!/usr/bin/env python
# coding: utf-8

# # Business Intelligence Analysis of Amazons Sales Data

# **Table of Contents**
# 
# 1. **[Introduction](#introduction)**
# 2. **[Data](#data)**
# 3. **[Sort](#sort)**

# ### Introduction
# <a name="introduction"></a>

# In this project i will be implementing techniques and statistics that I learned in my Business Intelligence skillpath on codecademy:
# 
# - **Q1** Top 10 most sold products
# - **Q2** Highest Rating products
# - **Q3** Most expensive products
# - **Q4** Total products in each category
# - **Q5** Top 5 Categories by Volume sold and Rough Revenue
# - **Q6** Is there any correlation between Price and Ratings
# - **Q7** Average price in categories.
# - **Q8** Create a more informative csv and excel file

# <a name="data"></a>
# # Import and Inspect Data

# In[11]:


#import the neccesary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[33]:


#import the dataset amazon.csv to az
az = pd.read_excel('wrangle-ing.xlsx')
az['actual_value_dollar'] = az['actual_value_dollar'].round(2)
az['discount_value_dollar'] = az['discount_value_dollar'].round(2)
print(az.head())


# We can see that the prices are reflected in the file with symbols, after investigation in excel, I saw that the currency recored in the data is in Indian Rupees, without hesitation, I popped into the "get info" button on the csv file and it showed me that the document was last modified 17 January 2023, after looking into global currencies I have chosen to display the Rupee as a value in Dollar (United States). 
# 
# I did so by looking at the Rupee around the week of 17 January 2023, and have decided on a solid 81 Rupee to Dollar exchange rate.
# 
# I did this within an Excel sheet, it is attached to this repository. 
# 
# We can see that the Dollar is being displayed with a chain of decimals despite showing up properly in excel to fix this we will round the dollar columns for this analysis.

# In[13]:


#check the info
print(az.info())


# In[14]:


#check the columns in az
print(az.columns)


# <a name="sort"></a>
# # Sort Data

# In[15]:


#Q1 top_10 (most sold products)
top_sold = az['product_name'].value_counts().reset_index()
top_sold.columns = ['product_name', 'count']
top_10_sold = top_sold.head(10)


# In[16]:


#Q2 highest_ratings
#make rating a float value as it is imported as an object number
az['rating'] = pd.to_numeric(az['rating'], errors='coerce')
sorted_ratings = az.sort_values(by='rating', ascending=False)[['product_id', 'product_name', 'rating']]


# In[17]:


#Q3 most_exp products (without discoounts)
sorted_exp = az.sort_values(by='actual_value_dollar', ascending=False)
#only return neccesary columns
sorted_exp = sorted_exp[['product_id', 'product_name', 'actual_value_dollar']]

most_exp_10 = sorted_exp.head(10)


# In[18]:


#Q4 total products in each category
category_counts = az.groupby('category')['product_name'].count().sort_values(ascending=False)


# In[19]:


#Q5 Top 5 Categories by Volume sold and Rough revenue (rough estimate!!)
#bc this data does not include a 'sales volume' column we will make a rough assumption based on the rating_count, taking into consideration that these values are not by any means a true reflection of the volume of sales.
az['rating_count'] = pd.to_numeric(az['rating_count'], errors='coerce') 
az['estimated_revenue'] = az['rating_count'] * az['actual_value_dollar']

#group by category and sum the rough estimated revenue
category_performance = az.groupby('category')['estimated_revenue'].sum().sort_values(ascending=False)
#create a dataframe
category_performance_df = category_performance.reset_index()

#column names
category_performance_df.columns = ['Category', 'Estimated_Revenue']

#format est_rev as money
category_performance_df['Estimated_Revenue'] = category_performance_df['Estimated_Revenue'].apply(lambda x: "${:,.2f}".format(x))


# In[22]:


print(az['actual_value_dollar'].dtype)
print(az['rating'].dtype)


# In[32]:


#Q6 Is there any correlation between Price and Ratings
#check the correlation for price and rating
corr_pr = az['actual_value_dollar'].corr(az['rating'])
print(corr_pr)


# In[45]:


#Q7 Avg price per category
#compare average prices across categories
compare_prices = az.groupby('category')['actual_value_dollar'].mean().reset_index().rename(columns={'actual_value_dollar': 'average_price'})
compare_prices = compare_prices.sort_values('average_price', ascending=False)


# In[46]:


#Q8 creating a more informative excel and csv file
columns = ['product_id', 'product_name', 'category', 'actual_value_dollar', 'discount_percentage', 'rating', 'rating_count', 'user_id', 'product_link']


# In[47]:


az_refined = az[columns]


# In[48]:


#export to csv
az_refined.to_csv('az_refined.csv', index=False)


# In[49]:


#export to excel file
az_refined.to_excel('az_refined.xlsx', index=False)

