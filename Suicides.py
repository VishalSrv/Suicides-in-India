
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib notebook')

scd=pd.read_csv('Suicides.csv')
ppn=pd.read_csv('population.csv',header=2)

ppn=ppn[['State Name','Name of City','Unnamed: 6','Unnamed: 7']]
ppn.rename(columns={'Unnamed: 6':'Males','Unnamed: 7':'Females'},inplace=True)
ppn.drop([0,496,497],inplace=True)
lt=[]
for i in ppn["Males"].values:
    i=i.replace(",","")
    lt.append(int(i))
lt2=[]    
for i in ppn["Females"].values:
    i=i.replace(",","")
    lt2.append(int(i))    
#ppn.drop("Males",axis=1,inplace=True)
ppn["Males"]=lt
#ppn.drop("Females",axis=1,inplace=True)
ppn["Females"]=lt2
ppn1=ppn.groupby('State Name')['Males'].agg({'total_males':np.sum})
ppn1.reset_index(inplace=True)
ppn2=ppn.groupby('State Name')['Females'].agg({'total_females':np.sum})
ppn2.reset_index(inplace=True)
ppn=pd.merge(ppn1,ppn2,how='inner',on='State Name')
ppn=ppn.rename(columns={'State Name':'State'})
scd=scd.where(scd['Total']!=0).dropna()
scd=scd.where(scd['Type']=='Failure in Examination').dropna()
scd=scd[(scd['Age_group']=='15-29')]
scd=scd[scd['Year']==2011]
scd1=scd[scd['Gender']=='Male']
scd2=scd[scd['Gender']=='Female']
scd1=scd1[['State','Total']]
scd2=scd2[['State','Total']]
scd1=scd1.rename(columns={'Total':'Males'})
scd2=scd2.rename(columns={'Total':'Females'})
scd=pd.merge(scd1,scd2,how='inner',on='State')
df=ppn.merge(scd,how='inner',on='State')
scd.set_index("State",inplace=True)
scd.rename(index={'A & N Islands':'Andaman & Nicobar Islands','Delhi (Ut)':'Delhi'},inplace=True)
scd=scd.reset_index()
scd['State']=scd['State'].apply(lambda x: x.upper())
df=pd.merge(scd,ppn,how='inner',on='State')
df['% male']=df['Males']/df['total_males']
df['% female']=df['Females']/df['total_females']
plt.figure(figsize=(14,14))
plt.plot(df['% male'],'-o',label='% male suicides in 2011')
plt.plot(df['% female'],'-',label='% female suicides in 2011')
plt.ylabel('% suicides')
plt.xlabel('States')
plt.title('% suicides of students(age group 15-29 year) in different states of India in year 2011 due to Failure in examination.',fontsize=10)
plt.legend()
ob=plt.gca()
df["State"].iloc[0]="A&N ISLAND"
lt3=list(df["State"].values)
ob.tick_params(bottom=False)
plt.xticks(np.arange(0,22),lt3,rotation=90,fontsize=8)
plt.show()



