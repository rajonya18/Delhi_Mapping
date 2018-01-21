import seaborn as sns; sns.set()
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

data=pd.read_csv("Delhi_mapping.csv")
data.drop(['Id','name','community mapped by name','community mapped by surname'],1,inplace=True)

for index,items in enumerate(data['community']):
    items=items[1:-1].split(',')
    temp=[]
    for j in items:
        j=j.strip().strip("'").strip()
        temp=temp+[j]
    data.iloc[index]['community']=temp

communities=[]
for item in data['community']:
    communities=list(set(communities+item))

pollStations=list(set(data['Polling Station Number']))
population=pd.DataFrame(columns=communities,index=pollStations)

for i in pollStations:
    for j in communities:
        population.loc[i][j]=0

for i in range(len(data)):
    s=data.iloc[i]['Polling Station Number']
    for j in data.iloc[i]['community']:
        population.loc[s][j]+=1

population.drop([''],axis=1,inplace=True)
population.fillna(value=0, inplace=True)
ax = sns.heatmap(population)

x=plt.gca().xaxis

for item in x.get_ticklabels():
    item.set_rotation(90)

y=plt.gca().yaxis

for item in y.get_ticklabels():
    item.set_rotation(0)

plt.show()
