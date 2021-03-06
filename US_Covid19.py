#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import Pandas module and alias as pd
import pandas as pd


# In[2]:


"""
read csv data from Github link across the time span from 1/22/20 to current: 
https://github.com/CSSEGISandData/COVID-19
"""
# read the US dataset: 'confirmed_US.csv', 'deaths_US.csv'
data = ['confirmed', 'deaths']
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'
suffix = '_US.csv'

# create a list combining the files above: dataList_us
dataList_us = []

# use for loop to complete the links individually
# put the complete links into the list of "dataList_us"
for i in range(len(data)):
    complete_url = url + data[i] + suffix
    df = pd.read_csv(complete_url)  
    print("Data about %s cases in the US:" %data[i])
    #have a glance at each Data Frame and put them into dataList_us
    display(df.head(5))
    # add the Data Frame into "dataList_us"
    dataList_us.append(df)


# In[3]:


"""
print the shapes of Data Frames(row x column) with string formatting
"""
# us_df_list[0]: US confirmed data
# us_df_list[1]: US deaths data
print("Shape (Rows, columns) of confirmed Data Frame: %s" %(dataList_us[0].shape,)) #.shape -> returns a tuple
print("Shape (Rows, columns) of deaths Data Frame: %s" %(dataList_us[1].shape,))


# In[4]:


"""
print the total days of observation about the US confirmed/ deaths data
"""
# to see what column index of "1/22/20" 
i = dataList_us[0].columns.get_loc("1/22/20") # output: 11 
# the date range from 1/22/20 to current: days
days_confirmed = dataList_us[0].shape[1] - (i+1)
print("%s days since the outbreak of covid 19 (1/22/20)" %str(days_confirmed)) # confirmed data's date range = US deaths data's date range


# In[5]:


"""
show the name of states and the number of states with enumerate()
"""
for index, state in enumerate(df.Province_State.unique()):
    print(index+1,state)


# In[6]:


"""
Data summarization: sum all the admins inside Data state into a single record
"""
# function to sum all the admins inside the same state into a single record
def sum_state(df, state):
    
    # query the rows matching the appointed state from the Data Frame
    df_state = df[df["Province_State"]==state]
    
    # create a new row to record the sum for each column: total
    total = df_state.sum(axis=0)
    
    # recover the values/contents of columns which were unnecessary to be calculated the sum 
    # the "Province_State" column will be marked as state name + "-> Sum" instead of solely state for recognizing later on .
    total.loc['UID'] = "NaN"
    total.loc['Admin2'] = "NaN"
    total.loc['FIPS'] = "NaN"
    total.loc['iso2'] = "US"
    total.loc['iso3'] = "USA"
    total.loc['code3'] = 840
    total.loc['Country_Region'] = "US"
    total.loc['Province_State'] = state + "-> sum"
    total.loc['Lat'] = df_state['Lat'].values[0]
    total.loc['Long_'] = df_state['Long_'].values[0]
    
    
    # append the new row to the original Data Frame and convert Series("sum_row") to Data Frame
    df = pd.concat([df, total.to_frame().T], ignore_index=True)
    # display the row of (df[df["Province_State"].str.contains(state + "-> sum")])
    df=df[df['Province_State'] != state]
    df.loc[df.Province_State == state + "-> sum", 'Province_State'] = state
    
    return df

# summarize the data of US confirmed cases and deaths cases by using "sum_admins_in_state" function above
for i in range(2):
    df = dataList_us[i] 
    for state in df.Province_State.unique():
        df = sum_state(df, state)
    dataList_us[i]=df

# have a look at the results such as the last 5 rows of the data
for i in range(len(data)):
    print("Data summarization about %s cases:" %data[i])
    display(dataList_us[i].tail(5))


# In[7]:


"""
Data simplification: delete the 6 unnecessary columns (UID	iso2	iso3	code3	FIPS	Admin2)
"""
# delete them from comfirmed dataset
us_confirmed = dataList_us[0]
us_confirmed = us_confirmed.drop(us_confirmed.iloc[:,:6], axis =1) # axis=1: represents columns
us_confirmed = us_confirmed.reset_index(drop=True) # recover the index of the Data Frame; drop=True:avoid the old index being added as a column

# delete them from deaths dataset
us_deaths = dataList_us[1]
us_deaths = us_deaths.drop(us_deaths.iloc[:,:6], axis =1)
us_deaths = us_deaths.reset_index(drop=True)


# have a look at the results such as the last 5 rows of the data
for i in range(len(data)):
    print("Data simplification about %s cases:" %data[i])
    if i==0:
        display(us_confirmed.tail(5))
    if i==1:
        display(us_deaths.tail(5))


# In[8]:


"""
Data organization: 
1. calculate the total cases of each state and date
2. create the death rate(%) column to "us_deaths" DataFrame and calculate it with map() and lambda
3. show the ratio of each state's death cases with pie chart
4. show the total confirmed/deaths cases per state with the higher order function - zip() 
5. revise the names of columns with higher order function such as map() and lambda
6. make a transpose of matrix after simplifying the data
7. calculate the daily addition of confirmed cases and plot it (add an average line in the plot)
8. data visualization - time series
9. Simple linear regression for predictions: y = mx+c (y: ttl confirmed cases; x: state's confirmed cases)  with inner function
"""

"""
1. calculate the total cases of each state and date
"""
# create a new row to summarize the US daily confirmed/ deaths cases everyday
us_confirmed.loc['Date Total']= us_confirmed.iloc[:,5:].sum()
us_deaths.loc['Total']= us_deaths.iloc[:,5:].sum() # including the summarization of population

# convert a float into an integer in a us_confirmed DataFrame
us_confirmed.iloc[:,5:] = us_confirmed.iloc[:,5:].astype(int)
# convert a float into an integer in a us_deaths DataFrame
us_deaths.iloc[:,5:] = us_deaths.iloc[:,5:].astype(int)

# have a look at the results such as the last 2 rows of the data
for i in range(len(data)):
    print("%s cases:" %data[i])
    if i==0:
        display(us_confirmed.tail(2))
    if i==1:
        display(us_deaths.tail(2))

# display the US confirmed dataset after the summarization
us_confirmed = us_confirmed.fillna("Summary") # fillna("Summary") -> replace NaN value to "Summary"
us_deaths = us_deaths.fillna("Summary") # fillna("Summary") -> replace NaN value to "Summary"

# have a look at the results such as the last 2 rows of the data
for i in range(len(data)):
    print("Data organization (after summarization) about %s cases:" %data[i])
    if i==0:
        display(us_confirmed.tail(2))
    if i==1:
        display(us_deaths.tail(2))


# In[9]:


"""
2. create the death rate(%) column and calculate it with map() and lambda
"""
# convert the column of us_deaths["Population"] to a list first
population_list = us_deaths["Population"].values.tolist()

# get the last column from "us_deaths" data which is the latest statistical date
deathNum_list = us_deaths[us_deaths.columns[-1:]].values.tolist() # 2D array

# flatten the 2D array to 1D array
from itertools import chain 
deathNum_list = list(chain.from_iterable(deathNum_list)) 

# calculate each state's death rate by using map() and lambda
m = map(lambda x,y: x/y*100 if y>0 else 0, deathNum_list,population_list[:])   

# round the death rate to 2 decimals by using map() and lambda again
rate_list = list(map(lambda x: round(x, ndigits=2) if x >0 else 0, list(m))) # list() -> convert the map objecct to a list

# create "Death Rate(%)" column in "us_deaths" DataFrame
us_deaths["Death Rate(%)"] = rate_list

# have a look at the results such as the last 3 rows of the data
us_deaths.tail(3) # the average death rate is on the bottom right corner 


# In[10]:


"""
3. show the ratio of each state's death cases with pie chart
"""
# import the module of plot
import matplotlib.pyplot as plt

labels = us_deaths["Province_State"][:-1] # labels: the states of US
sizes = us_deaths.iloc[:-1,-2:-1].iloc[:, 0].tolist() # sizes: the list of ystd's death cases of each state
plt.figure(figsize=[30, 30]) # set the size of plot 

explode = [] # explode: the list of the different shapes in the plot
for i in range(58):
    if i % 3 == 0:
        explode.append(0.15)
    elif i % 2 ==0:
         explode.append(0.07)
    else:
        explode.append(0)

plt.pie(sizes, labels=labels,autopct='%1.1f%%', explode=explode)
plt.title('Death cases of each state', fontsize=30, y=1.05)

plt.show()


# In[11]:


"""
4-1. Show the total confirmed cases per state with the higher order function with zip() 
"""
# the column of us_confirmed["Province_State"]: zip_1
zip_1 = us_confirmed["Province_State"]

# the column of us_confirmed["State Total"]: zip_2
zip_2 = us_confirmed.iloc[:,-1] # list type: int

# Zip through zip_1 and zip_2 and pair them together
zipped = zip(zip_1,zip_2)

print("Total confirmed cases per state in ascending order:")
# sort the zipped list
sorted(zipped, key = lambda t: t[1])


# In[12]:


"""
4-2. Show the total deaths cases per state with the higher order function with zip() 
"""
# the column of us_deaths["Province_State"]: zip_1
zip_1 = us_deaths["Province_State"]

# the column of us_deaths["State Total"]: zip_2
zip_2 = us_deaths.iloc[:,-2] # list type: float 

# the column of us_deaths["Death Rate(%)"]: zip_3
zip_3 = us_deaths.iloc[:,-1]

# Zip through zip_1 and zip_2 and pair them together
zipped = zip(zip_1,zip_2,zip_3)

print("Total deaths cases and rate(%) per state in ascending order of death rate:")
# sort the zipped list
sorted(zipped, key = lambda t: t[2])


# In[13]:


"""
5-1. revise the names of columns with higher order function such as map() and lambda to add "_confirmed" after every provice states
"""
# make a list of province states from us_confirmed: provinceList
provinceList = list(us_confirmed["Province_State"]) 

# use the higher order function(map()) and lambda 
# to append "_Confirmed" to each element in provinceList: map_confirmed
map_confirmed = map(lambda x: (str(x) + "_confirmed"), provinceList)

# to make map_confirmed a list
state_confirmed = list(map_confirmed)
state_confirmed


# In[14]:


"""
5-2. revise the names of columns with higher order function such as map() and lambda to add "_deaths" after every province states
"""
# make a list of province states from us_confirmed: provinceList
provinceList = list(us_deaths["Province_State"]) 

# use the higher order function(map()) and lambda 
# to append "_Confirmed" to each element in provinceList: map_confirmed
map_deaths = map(lambda x: (str(x) + "_deaths"), provinceList)

# to make map_confirmed a list
state_deaths = list(map_deaths)
state_deaths


# In[15]:


"""
6-1. make a transpose of matrix after simplifying the data of confirmed cases
"""
# remove the first 5 unnecessary columns of us_confirmed which are Province_State	Country_Region	Lat	Long_	Combined_Key: data_confirmed
data_confirmed = us_confirmed.iloc[:,5:]

# name data_confirmed's index after state_confirmed's elements
data_confirmed.index = pd.Index(state_confirmed, name='Date(M/D/Y)')

# make a transpose of data_confirmed to change the positions of date and province_confirmed
data_confirmed = data_confirmed.T

# have a look at the last 5 rows of data_confirmed
data_confirmed.head(10)


# In[16]:


"""
6-2. make a transpose of matrix after simplifying the data of deaths cases
"""
# remove the first 5 unnecessary columns of us_confirmed which are Province_State	Country_Region	Lat	Long_	Combined_Key: data_deaths
data_deaths = us_deaths.iloc[:,5:]

# name data_deaths's index after state_confirmed's elements
data_deaths.index = pd.Index(state_deaths, name='Date(M/D/Y)')

# make a transpose of data_deaths to change the positions of date and province_confirmed
data_deaths = data_deaths.T

# have a look at the first 5 rows of df1
data_deaths.tail(5)


# In[17]:


"""
7-1. calculate the daily addition of confirmed cases
"""
data_confirmed["Daily Addition"] = 0
data_confirmed.head(3)


for index in range(data_confirmed.shape[0]-1,-1,-1):
        if index == 0:
            data_confirmed.iloc[index,-1] = data_confirmed.iloc[index,-2]
        else:
            data_confirmed.iloc[index,-1] = data_confirmed.iloc[index,-2] - data_confirmed.iloc[index-1,-2]

data_confirmed.head(3)


# In[18]:


"""
7-2. plot the daily addition and add an average line in the plot
"""
# import matplotlib.pyplot and alias as plt
import matplotlib.pyplot as plt
import numpy as np

# find the mean of daily addition
mean = data_confirmed["Daily Addition"].mean()

# set up the plot
fig,ax= plt.subplots(figsize=(12,8))

# plot the data
data_confirmed["Daily Addition"].plot()
ax.axhline(mean) # axhline() -> to add a horizontal line across the axis
plt.show()


# In[19]:


"""
8. Data visualization - time series
"""
# delete the last row (State Total) to make a time series later
data_confirmed.drop(data_confirmed.tail(1).index, inplace = True) # inplace = True -> revise the original object instead of creating a new object
data_confirmed.tail(5)


# In[20]:


# prepare the list of df1's index(date) for the plot: df1_index
data_confirmed_index = data_confirmed.index.tolist()

# make df1's index same as to_datetime(df1_index)
data_confirmed.index = pd.to_datetime(data_confirmed_index)# to_datetime() helps to convert string Date time into Python Date time object

# set to_datetime(df1_index) as the index of the Data Frame(df1)
data_confirmed.set_index(data_confirmed.index, inplace=True) # inplace=True -> the data is revised in place.

# make a plot to show the number of confirmed cases of each state
data_confirmed.plot(y = state_confirmed[:-1], use_index = True, title='Curve Graph', style='--').legend(loc='upper left',shadow=True) # state_confirmed[:-1] -> not select the last column(Summary_confirmed) of the state_confirmed list; use_index = True -> use index as ticks for x axis(use_index: default True actually); legend: an area describing the elements of the graph.
plt.gcf().set_size_inches(25, 18) # set the figure size in inches (1in == 2.54cm)

# equalize the scale of x-axis and y-axis
plt.axis(aspect='equal')

# name the label of x and y
plt.xlabel('Time')
plt.ylabel('Cases #')

# display the plot
plt.show()


# In[21]:


# use the subplots to display each state's status
axes = data_confirmed.plot(kind='bar',figsize=(30,40), use_index = True, title='Bar Chart', subplots=True, layout=(12,5))
plt.show()


# In[22]:


"""
9. Simple linear regression for predictions: y = mx+c (y: ttl confirmed cases; x: state's confirmed cases) with inner function
Note: higher coefficients indicate greater relevance of the predictor
Note: x = Independent Variable; y = Dependent Variable
"""

def coefficient(state,ttl):
    # collecting the training data of X and Y
    X = data_confirmed[state].values 
    Y = data_confirmed[ttl].values

    # mean X and Y
    mean_x = np.mean(X)
    mean_y = np.mean(Y)
 
    # ttl number of values
    n = len(X)
 
    # Using the formula to calculate m and c
    numer = 0
    denom = 0
    for i in range(n):
        numer += (X[i] - mean_x) * (Y[i] - mean_y)
        denom += pow((X[i] - mean_x),2)
        m = numer / denom
        c = mean_y - (m * mean_x)
    
    # Print coefficients
    print("TTL confirmed num = c(%s) + m(%s) ??? %s num" %(c, m, state))
    
    # inner function to make the plot of simple linear regression
    def draw(X,Y,c,m):
        plt.figure(figsize=(20,10)) 

        # plotting values and regression line
        max_x = np.max(X) + 100
        min_x = np.min(X) - 100
        
        # create the prediction space
        x = np.linspace(min_x, max_x)
        
        # create a simple linear regression 
        y = c + m * x 
 
        # ploting line
        plt.plot(x, y, color='g', label='regression line', lw = 4) # lw = linewidth
        
        # ploting scatter points
        plt.scatter(X, Y, c='r', label='training data')
        
        
        # make a plot
        plt.xlabel('%s cases #' %state)
        plt.ylabel('Total confirmed cases #')
        plt.legend()
        plt.show()
    
    # call the inner function
    draw(X,Y,c,m)

    


# substitute the state's confirmed data into the function above to draw a SLR 
for i in list(data_confirmed.columns):
    coefficient(i,"Summary_confirmed")


# In[ ]:


"""
Lastly, send this whole code to user's email
"""
# import the email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# create the object of MIMEMultipart
content = MIMEMultipart()  

# allow user to input the email (string type)
email = str(input("Your email address: "))

# email title
content["subject"] = "Happy Chinese New Year! Code is here!"

# sender
content["from"] = "vicky.kuo.contact@gmail.com"

# receiver
content["to"] = email

# write the email body
content.attach(MIMEText("Happy Chinese New Year!! Please refer to the whole code here: https://codeshare.io/adqx0K"))

# import the SMTP module
import smtplib

# set SMTP server
with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
    try:
        # verify the SMTP server
        smtp.ehlo()
        # encrypted transmission
        smtp.starttls()
        # login sender's email
        smtp.login("medium.fob.contact@gmail.com", "ejxfsttvtjhuwvlm")
        # send the email
        smtp.send_message(content)
        print("Email sent.")
    except Exception as e:
        print("Error message: ", e)


# In[ ]:




