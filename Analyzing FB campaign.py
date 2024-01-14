#!/usr/bin/env python
# coding: utf-8

# ## Step 1: Examine the Dataset

# In[67]:


import pandas as pd
df = pd.read_csv(r"C:\Users\user\Desktop\A Marketing campaign Dataset.csv")
df.head()


# In[68]:


df.info()


# ## Step 2: Campaign Highlights

# In[69]:


df[["Reach","Impressions","Link Clicks","Landing Page Views","Results","Amount Spent"]].sum()


# ## Campaign Highlights
# 
# 1. We reached around 450K unique people.
# 2. Approx 1.1 million impressions.
# 3. Each person saw the ad around 2.5 times.
# 4. Approx 5.6K link clicks and 2.9K landing page views.
# 5. Total of 83 results.
# 6. Spent 4,362 EUR.

# ## Step 3: Ad Set Overview

# In[6]:


(df['Ad Set Name']).unique()


# ### Hot, Warm, and Cold Ad Sets

# In[70]:


def categorize_ad_set(ad_set_name):
    if 'Warm' in ad_set_name:
        return 'Warm'
    elif 'HOT' in ad_set_name:
        return 'Hot'
    else:
        return 'Cold'

df['Category'] = df['Ad Set Name'].apply(categorize_ad_set)
df.head()


# In[72]:


results = df.groupby('Category').agg({'Reach':'mean','Impressions':'mean',
                                    'CTR (all)':'mean','Results':'mean',
                                    'CPR':'mean'})

results


# ### Looalike vs Detailed Targeting

# In[20]:


df['Ad Set Name'].unique()


# In[73]:


def categorize_ad_set_2(ad_set_name):
    if('DT' in ad_set_name):
        return 'Detailed Targeting'
    elif('LLA' in ad_set_name):
        return 'Lookalike Audience'
    else:
        return 'Other'

df['Subcategory'] = df['Ad Set Name'].apply(categorize_ad_set_2)


# In[74]:


df_cold = df[df['Category']=='Cold']


# In[75]:


df_cold = df_cold.groupby('Subcategory').agg({'Reach':'mean','Impressions':'mean',
                                    'CTR (all)':'mean','Results':'mean',
                                    'CPR':'mean'})

df_cold


# In[76]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[77]:


df_transformed = df_cold.reset_index().melt('Subcategory')
df_transformed


# In[83]:


viz = sns.FacetGrid(df_transformed, col='variable', col_wrap=3, sharex=False,
                   sharey=False, height=4)

viz.map(sns.barplot, 'Subcategory', 'value', order=df_cold.reset_index()['Subcategory'])

plt.show()


# ## Step 4: Detailed Ad Set Analysis

# ### Hot

# In[84]:


df_hot = df[df['Category']=='Hot']
df_hot = df_hot.reset_index()
df_hot


# ### Top-Funnel Metrics

# In[89]:


def top_funnel_metrics(df):
    fig,axs = plt.subplots(1, 3, figsize=(23,5))
    
    sns.barplot(x='Ad Set Name', y='Reach', data=df, ax=axs[0])
    axs[0].set_title('Reach')
    
    sns.barplot(x='Ad Set Name', y='Impressions', data=df, ax=axs[1])
    axs[1].set_title('Impressions')
    
    sns.barplot(x='Ad Set Name', y='CPM', data=df, ax=axs[2])
    axs[2].set_title('CPM')
    
    for ax in axs:
        for label in ax.get_xticklabels():
            label.set_rotation(90)
            
    plt.show()
    
top_funnel_metrics(df_hot)


# ### Mid-Funnel Metrics

# In[90]:


def mid_funnel_metrics(df):
    fig, axs = plt.subplots(1, 3, figsize=(23,5))
    
    sns.barplot(x='Ad Set Name', y='CTR (all)', data=df, ax=axs[0])
    axs[0].set_title('CTR (all)')
    
    sns.barplot(x='Ad Set Name', y='Landing Page Views', data=df, ax=axs[1])
    axs[1].set_title('Landing Page Views')
    
    sns.barplot(x='Ad Set Name', y='CPC', data=df, ax=axs[2])
    axs[2].set_title('CPC')
    
    for ax in axs:
        for label in ax.get_xticklabels():
            label.set_rotation(90)
    
    plt.show()
    
mid_funnel_metrics(df_hot)


# ### Bottom-Funnel Metrics

# In[91]:


def bottom_funnel_metrics(df):
    fig, axs = plt.subplots(1, 2, figsize=(23,5))
    
    sns.barplot(x='Ad Set Name', y='Results', data=df, ax=axs[0])
    axs[0].set_title('Results')
    
    sns.barplot(x='Ad Set Name', y='CPR', data=df, ax=axs[1])
    axs[1].set_title('CPR')
    
    for ax in axs:
        for label in ax.get_xticklabels():
            label.set_rotation(90)
    
    plt.show()
    
bottom_funnel_metrics(df_hot)


# In[92]:


sns.barplot(x='Ad Set Name', y='Amount Spent', data=df_hot)


# ### Warm

# In[93]:


df_warm = df[df['Category']=='Warm']
df_warm = df_warm.reset_index()


# In[94]:


top_funnel_metrics(df_warm)


# In[95]:


mid_funnel_metrics(df_warm)


# In[96]:


sns.barplot(x='Ad Set Name', y='Link Clicks', data=df_warm)


# In[97]:


bottom_funnel_metrics(df_warm)


# ### Cold

# In[98]:


df_cold = df[df['Category']=='Cold']
df_cold = df_cold.reset_index()


# In[99]:


def all_cold_adsets(df, metrics, ad_set_types=['Lookalike Audience','Detailed Targeting']):
    
    fig, axes = plt.subplots(nrows=len(metrics), ncols=len(ad_set_types), 
                             figsize=(12,11), sharey='row')
    
    for i, metric in enumerate(metrics):
        for j, ad_set_type in enumerate(ad_set_types):
            filtered_df = df[df['Subcategory']==ad_set_type]
            ax = axes[i,j]
            sns.barplot(x='Ad Set Name', y=metric, data=filtered_df, ax=ax)
            ax.set_title(f'{metric}-{ad_set_type}')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            
    plt.tight_layout()
    plt.show()


# In[64]:


top_funnel_metrics = ['Reach', 'Impressions', 'CPM']
all_cold_adsets(df_cold, top_funnel_metrics)


# ### Mid-Funnel Metrics

# In[100]:


mid_funnel_metrics = ['CTR (all)','CPC','Landing Page Views']
all_cold_adsets(df_cold, mid_funnel_metrics)


# ### Bottom-Funnel Metrics

# In[102]:


bottom_funnel_metrics = ['Results','CPR','Amount Spent']
all_cold_adsets(df_cold, bottom_funnel_metrics)


# In[ ]:




