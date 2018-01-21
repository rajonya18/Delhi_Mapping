
import numpy as np
from ipywidgets.embed import embed_minimal_html
from matplotlib import pyplot as plt
from googlemaps import Client
import pandas as pd
from mpl_toolkits.basemap import Basemap
import googlemaps
import gmaps

def findPos(pollStations,data):

    gmaps = googlemaps.Client(key='AIzaSyA-Mb5xxYe0XkHkkoEMl_YqbRjCcnwQjRY')
    positions=pd.DataFrame(columns=['lat','lon'],index=pollStations)
    for i in pollStations:
        geocode_result = gmaps.geocode(i)
        positions.loc[i]['lat'] = geocode_result[0]["geometry"]["location"]["lat"]
        positions.loc[i]['lon'] = geocode_result[0]["geometry"]["location"]["lng"]

    return positions

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



positions=findPos(pollStations , data)
gmaps.configure('AIzaSyBwEyjaABv6E1VJK3P_GKmMrvCIs8QEBJI')
locations=[positions['lat'],positions['lon']]
weight=population['english']
fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations, weights=weight))
embed_minimal_html('export.html', views=[fig])
