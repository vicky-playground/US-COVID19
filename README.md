<img src="https://user-images.githubusercontent.com/90204593/133143634-eb65b12a-014d-4242-8b09-53b8e549a8a5.png" width="320"> <img src="https://user-images.githubusercontent.com/90204593/133143664-97f29f5f-9e6c-4856-85dd-32b9d97cd96b.png" width="350"> <img src="https://user-images.githubusercontent.com/90204593/133143677-af73a5f2-d5d6-4f44-a26e-e115dd73ce5c.png" width="350">


About the project
=
Implement the analysis of time series with Python and practice to use SMTP to send the code to emails:
1. Read csv data from Github link across the time span from 1/22/20 to current: 
https://github.com/CSSEGISandData/COVID-19
2. Read and organize the dataset 
3. Data summarization: sum all the admins inside the same state into a single record
4. Data simplification: delete the unnecessary columns 
5. Data organization: 
  * calculate the total cases of each state and date
  * create the death rate(%) column to "us_deaths" DataFrame and calculate it with map() and lambda
  * show the ratio of each state's death cases with pie chart
  * show the total confirmed/deaths cases per state with the higher order function - zip() 
  * revise the names of columns with higher order function such as map() and lambda
  * make a transpose of matrix after simplifying the data
  * calculate the daily addition of confirmed cases and plot it (add an average line in the plot)
  * data visualization - time series
  * Simple linear regression for predictions: y = mx+c (y: ttl confirmed cases; x: state's confirmed cases)  with inner function
6. Lastly, send this whole code to user's email

Project setup
=
    import pandas 
    from itertools import chain 
    import matplotlib.pyplot 
    import matplotlib.pyplot 
    import numpy 
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
