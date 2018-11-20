from requests import get
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import pymysql
from pandas.io import sql
from sqlalchemy import create_engine

##url='https://www.yelp.com/c/seattle/physicians'
url='https://www.iitk.ac.in/hc/specialist-opd-doctor-s-list'

response=get(url)

##print(response.text.encode("utf-8"))

html_soup=BeautifulSoup(response.text.encode("utf-8"),'lxml')
divdata=html_soup.find('div',{'class' : 'facoverview'})


#extract the doctor details table
Table_Data=divdata.find('table')

#paragraph containing details
Para_Data=Table_Data.find_all('p')

#Lists to store the scraped data in
name=[]
day=[]
department=[]
no_of_patient=[]
time=[]
c=0
k=0
for d in Para_Data:
	if k>4:
		#The name
		if c==0:
			name.append(d.text)
			c+=1
		#The Days on which Available
		elif c==1:
			day.append(d.text)
			c+=1
		#The department
		elif c==2:
			department.append(d.text)
			c+=1
		#No of Patient 
		elif c==3:
			no_of_patient.append(d.text)
			c+=1
		#Time
		elif c==4:
			time.append(d.text)
			c=0
	else:
		k+=1

#Converting List to DataFrame
df=pd.DataFrame()
df['Name of doctors']=name
df['day']=day
df['department']=department
df['no_of_patient']=no_of_patient
df['time']=time

#Saving DataFrame to Database
table_name=raw_input("Enter Table name To store Scrapped Data::")

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",#username
                               pw="",#password
                               db="web_scrapped_data"))
df.to_sql(con=engine, name=table_name, if_exists='replace')

R_df = pd.read_sql('SELECT * FROM '+table_name, con=engine)
print R_df	


	

	




