from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
from pandas.io import sql
from sqlalchemy import create_engine
import re


Web_Url='https://refadoc.com/doctors/mumbai/gynecologist'

response=get(Web_Url)

##print(response.text.encode("utf-8"))

html_soup=BeautifulSoup(response.text.encode("utf-8"),'lxml')


#Lists to store the scraped data in
review=[]
Data_l=[]
qualification=[]
Area=[]
Address=[]

#Extract the details of all Doctors
Data_Containers=html_soup.find_all('div',{'class' : 'col-md-7 hs-doctor-result'})
for Data in Data_Containers:
	#The Name 
	Data_l.append(Data.h3.text)
	
	#the Review
	r=Data.find('span',{'class' : 'views'})
	review.append(r.text)
	
	#Other Information
	datalist=Data.find_all('div',{'class' : 'result-info'})
	f=1
	for data in datalist:
		index=data.text.index(':')
		str=data.text[index+1:]
		f+=1
		
		#The Qualification
		if data.text.__contains__("Qualification :"):
			str=re.sub(r'[..]+','',str)
			qualification.append(str)
			
		#The Area
		elif data.text.__contains__("Area :"):
			Area.append(str)
			
		#The Address	
		elif data.text.__contains__("Address :"):
			str=re.sub(r'[..]+','',str)
			Address.append(str)
	if f!=4:
		qualification.append("----")


#Converting List to DataFrame
df=pd.DataFrame()
R_df=pd.DataFrame()
df['Data of doctors']=Data_l
df['qualification']=qualification
df['Area']=Area
df['Address']=Address
df['review']=review

table_name=raw_input("Enter Table name To store Scrapped Data::")

#Saving DataFrame to Database
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="web_scrapped_data"))
df.to_sql(con=engine, name=table_name, if_exists='replace')

R_df = pd.read_sql('SELECT * FROM '+table_name, con=engine)
print R_df	
			
		

	
	

