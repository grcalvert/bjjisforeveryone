# -*- coding: utf-8 -*-
#Gray Calvert  grayrc1@yahoo.com


#-----------------------------------Please READ ASSUMPTIONS----------------------------------------
#left Albany out of the analysis.  It was not available in the population data.
#Covington and Windsor Locks were not in the population data, used Cincinnati and Hartford population instead.  
#only included one Washington from the temp data
#missing data was backfilled
#email:  eric@synmax.com

import pandas as pd
from matplotlib import pyplot as plt
#----------pulls data into Pandas DF-------------------------------------------------------------------------
path = r'C:\Users\Gray Calvert\Downloads\coding'
file1 = 'Population Data.csv'
file2 = 'Temperature Data.csv'
df_pop1 = pd.read_csv(path+'\\'+file1).iloc[:,0:3]
df_temp1 = pd.read_csv(path+'\\'+file2)
df_temp1['location_date']=pd.to_datetime(df_temp1['location_date'])
df_pop = df_pop1.sort_values(by='City')
df_temp2 = df_temp1.sort_values(by='name')
df_temp=df_temp2[~df_temp2['name'].isin(['Washington'])] 

#--------------------Create Global Variables----------------------------------------------------------------
dates =  pd.date_range('2015-01-01','2021-04-20') #dates to be used as index column in main df

#list of population cities  to match to temperature cities
pop_cities = ['Atlanta', 'Baltimore', 'Boise', 'Boston', 'Buffalo', 'Burbank','Chicago', 'Columbus_OH', 'Cincinnati', 
              'Dallas', 'Denver','Detroit', 'Fresno', 'Houston', 'Las Vegas', 'Little Rock', 'Los Angeles', 'Memphis', 
              'Minneapolis', 'New York','Nashville', 'New Orleans', 'Philadelphia', 'Phoenix', 'Pittsburgh','Portland', 
              'Raleigh', 'Richmond_VA', 'Sacramento','Salt Lake City', 'San Francisco', 'Seattle', 'Spokane', 'St. Louis', 
              'Washington','Hartford'] 

season_dict = {1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}

###-------------------------------FUNCTION------------------------------------------------------------
#-----------------------incorportates max, min and mean temps from the data--------------------------------------
#-----------------------reorganizes data with cities across x axis and dates on the y axis------------------
#----multiplies temp by (city pop/total pop of cities) to create a weighted average.  Then sums the cities wa for each each date (row)
#-----------------------back fills missing data-----------------------------------------------------------------
#-----------------------creates dictionaries to map city names (temp and pop) and population from data sources---------------------
#-----------------------groups data by month and season----------------------------------------------------------

def temp(temp_type,period): #"temp_min_c", "temp_max_c", "temp_mean_c"
    df_temp_pivot = pd.pivot_table(df_temp, values=temp_type, index=["location_date"], columns=["name"])
    df_temp_new = pd.DataFrame(index=dates)
    df2 = df_temp_new.join(df_temp_pivot,how='outer')
    df2_fillna = df2.iloc[:,1:].fillna(method = 'bfill') #backfill missing temp data. Does not include Albany
    cities = df2_fillna.columns #cities from temp data, which become the column heads in the final df
    temp_cities = cities #cities but does not include Albany
    e=df_pop[df_pop['City'].isin(pop_cities)] #filter to pull only the cities in pop data needed for temp
    pop = e['population'].to_list()  #population list
    city = e['City'].to_list()
    g_dict=dict(zip(temp_cities,pop_cities))
    h_dict=dict(zip(city,pop))
    df_final = df2_fillna.copy()
    for column in df_final: 
        df_final[column] = df_final[column].apply(lambda x: x*(h_dict[g_dict[column]]/sum(pop)))
    df_final['row_sum'] = df_final.sum(axis=1)
    df_final['month'] = pd.to_datetime(df_final.index).month
    df_final['season'] = df_final['month'].apply(lambda x:season_dict[x])
    df_final_group = df_final.groupby(period).row_sum.mean()
    return df_final_group

#creates DFs for plots
mean_month = temp("temp_mean_c","month")
max_month = temp("temp_max_c","month")
min_month = temp("temp_min_c","month")
temp_month = pd.concat([mean_month,max_month,min_month],axis=1)
temp_month.columns = ['temp_mean','temp_max','temp_min']

mean_season = temp("temp_mean_c","season")
max_season = temp("temp_max_c","season")
min_season = temp("temp_min_c","season")
temp_season = pd.concat([mean_season,max_season,min_season],axis=1)
temp_season.columns = ['temp_mean','temp_max','temp_min']

#---------------------------------Check for missing data-----------------------------------------------

df_temp_pivot = pd.pivot_table(df_temp, values="temp_mean_c", index=["location_date"], columns=["name"])
df_temp_new = pd.DataFrame(index=dates)
df2 = df_temp_new.join(df_temp_pivot,how='outer')
null=df2.isnull().sum()

print(null)
print(df2.shape)
print(null.mean())

#------------------------------PLOTTING------------------------------------------------------------

print(temp_season.plot()) #seasonal graph
print(temp_month.plot()) #monthly graph

#Plots the missing temp data as a comparison to the total number of rows.  It emphasizes missing data is very small and not significant
df_missing_data = pd.DataFrame([null.mean(),df2.shape[0]])
df_missing_data.index=['missing data','total rows in data set']
df_missing_data.plot(kind='bar',stacked=True, title='missing data');



