# -*- coding: utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt
#C:\Users\Gray Calvert\Downloads\coding

path = r'C:\Users\Gray Calvert\Downloads\coding'
file1 = 'Population Data.csv'
file2 = 'Temperature Data.csv'
df_pop1 = pd.read_csv(path+'\\'+file1).iloc[:,0:3]
df_temp1 = pd.read_csv(path+'\\'+file2)#,usecols = [0,5,6,7,8])#,index_col = 'name')
df_temp1['location_date']=pd.to_datetime(df_temp1['location_date'])
df_pop = df_pop1.sort_values(by='City')
df_temp2 = df_temp1.sort_values(by='name')
df_temp=df_temp2[~df_temp2['name'].isin(['Washington'])] 


df_temp_pivot = pd.pivot_table(df_temp, values="temp_mean_c", index=["location_date"], columns=["name"])

dates =  pd.date_range('2015-01-01','2021-04-20')

df_temp_new = pd.DataFrame(index=dates)

df2 = df_temp_new.join(df_temp_pivot,how='outer')

#backfill without Albany
df2_fillna = df2.iloc[:,1:].fillna(method = 'bfill')

null=df2.isnull().sum()
null2=df2_fillna.isnull().sum()
#print(null2)


##------ lists to create two dicts----1 dict is city temp:city pop and other dict is city pop:pop #s-----------

cities = df2_fillna.columns #cities from temp data, which become the column heads in the final df
temp_cities = cities #cities but does not include Albany
#had to create this from eyeballing cities temp columns
pop_cities = ['Atlanta', 'Baltimore', 'Boise', 'Boston', 'Buffalo', 'Burbank','Chicago', 'Columbus_OH', 'Cincinnati', 
              'Dallas', 'Denver','Detroit', 'Fresno', 'Houston', 'Las Vegas', 'Little Rock', 'Los Angeles', 'Memphis', 
              'Minneapolis', 'New York','Nashville', 'New Orleans', 'Philadelphia', 'Phoenix', 'Pittsburgh','Portland', 
              'Raleigh', 'Richmond_VA', 'Sacramento','Salt Lake City', 'San Francisco', 'Seattle', 'Spokane', 'St. Louis', 
              'Washington','Hartford'] #these are cities from population data

e=df_pop[df_pop['City'].isin(pop_cities)] #filter to pull only the cities in pop data needed for temp

pop = e['population'].to_list()  #population list
city = e['City'].to_list()
print(sum(pop))




## -----------------------------dictionary creation----------------------------

g_dict=dict(zip(temp_cities,pop_cities))
h_dict=dict(zip(city,pop))
quarter_dict = {1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}

#--------------------------------FINAL DF-------------------------




df_final = df2_fillna.copy()
for column in df_final: 
    #df_final[g_dict[key]] = df_final[g_dict[key]].apply(lambda x: x*([g_dict[key]][1]/sum(pop)))
    df_final[column] = df_final[column].apply(lambda x: x*(h_dict[g_dict[column]]/sum(pop)))
    
df_final['row_sum'] = df_final.sum(axis=1)
df_final['month'] = pd.to_datetime(df_final.index).month
df_final['quarter'] = df_final['month'].apply(lambda x:quarter_dict[x])


#---------------------------------GROUP MONTH and QUARTER--------------------------------------

df_final_month = df_final.groupby('month').row_sum.mean()
df_final_quarter = df_final.groupby('quarter').row_sum.mean()
print(df_final_month.plot())


#------------------------------PLOTTING------------------------------------------------------------




#left Albany out
#Cincinnati for covington
#Hartford for Windsor Locks

