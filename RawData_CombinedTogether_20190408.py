#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd 


# In[2]:


# read in all the raw files 
control = pd.read_csv('manipulated_data_control_full.csv')
publicgood = pd.read_csv('manipulated_data_publicgood_full.csv')
evaluation = pd.read_csv('manipulated_data_evaluation_full.csv')


# In[3]:


# Make column indicating which treatment they were in 
control['treatment']=['control']*len(control)
publicgood['treatment']=['publicgood']*len(publicgood)
evaluation['treatment']=['evaluation']*len(evaluation)


# In[4]:


all_together = pd.concat([control, publicgood, evaluation], axis=0).reset_index(drop=True)


# In[5]:


# add score label 
correct = []

for index, row in all_together.iterrows(): 
    if (row['answer']==row['animal_present']): 
        correct.append(1)
    else: 
        correct.append(0)

all_together['correct']=correct


# In[6]:


all_together.head()


# In[7]:


all_together.to_csv('combined_raw_data_nodrop_20190407.csv', index=False)
# This is the raw combined data 


# In[8]:


# manipulated by worker 

controlonly = all_together[all_together['treatment']=='control'].reset_index(drop=True) 
publicgoodonly = all_together[all_together['treatment']=='publicgood'].reset_index(drop=True)
evaluationonly = all_together[all_together['treatment']=='evaluation'].reset_index(drop=True)


# In[10]:


# for each worker, let's create their score, and also append their information 

controlonly.columns

# information columns: 
# ['_started_at','_channel','_trust','_country','_region','_city','_ip']


# In[24]:


def create_score_by_worker(df): 
    workers = list(df['_worker_id'].unique()) 
    info_df = df[['_worker_id','_channel','_trust','_country','_region','_city','_ip','treatment']].drop_duplicates()
    row = []
    for w in workers: 
        subdf=df[df['_worker_id']==w].reset_index(drop=True)
        score = np.nansum(subdf['correct'])/len(subdf)
        row.append({'_worker_id': w, 'score': score})
    output_df = pd.DataFrame(row).reset_index(drop=True)
    return(output_df.merge(info_df, how='left', on='_worker_id'))


# In[26]:


control_workers = create_score_by_worker(controlonly)


# In[27]:


publicgood_workers = create_score_by_worker(publicgoodonly)


# In[28]:


evaluation_workers = create_score_by_worker(evaluationonly)


# In[33]:


# concatenate together 
allworkers = pd.concat([control_workers, publicgood_workers, evaluation_workers]).reset_index(drop=True)
allworkers.to_csv('combined_scores_by_worker.csv', index=False)


# In[ ]:


# And we have bloody compliance to do...

