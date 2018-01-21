from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import googlemaps
from mpl_toolkits.basemap import Basemap


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

ll_lat=200
ll_lon=200
ur_lat=-200
ur_lon=-200

positions=findPos(pollStations , data)
for i in range(len(positions)):
    if positions.iloc[i]['lat']<ll_lat:
        ll_lat=positions.iloc[i]['lat']
    elif positions.iloc[i]['lat']>ur_lat:
        ur_lat=positions.iloc[i]['lat']

    if positions.iloc[i]['lon']<ll_lon:
        ll_lon=positions.iloc[i]['lon']
    elif positions.iloc[i]['lon']>ur_lon:
        ur_lon=positions.iloc[i]['lon']

print ll_lat
print ll_lon
print ur_lat
print ur_lon

m=Basemap(projection='mill',llcrnrlat=ll_lat,llcrnrlon=ll_lon,urcrnrlat=ur_lat,urcrnrlon=ur_lon)
m.drawcoastlines()

plt.show()
