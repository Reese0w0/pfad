import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
from scraping_utils import get_url

URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

prs = {
    'format': 'geojson',
    'starttime': '2024-01-01',
    'endtime': '2024-06-01',
    'minmagnitude': 5,
    'orderby': 'time'
}


response = get_url(URL,filename,prs)

if response.status_code == 200:
    data = response.json()
    earthquakes = data['features']

    earthquake_data = []

    for eq in earthquakes:
        properties = eq['properties']
        geometry = eq['geometry']
        depth = geometry['coordinates'][2]
        timestamp_ms = properties['time']

        timestamp_s = timestamp_ms / 1000
        dt_object = datetime.datetime.fromtimestamp(timestamp_s)

        earthquake_data.append([
            dt_object,
            properties['place'],
            properties['mag'],
            depth,
            properties['url']
        ])

    df = pd.DataFrame(earthquake_data, columns=['Time', 'Location', 'Magnitude', 'Depth', 'URL'])
    df.to_csv('usgs_earthquake_data.csv', index=False)
    print("successfully into 'usgs_earthquake_data.csv'")

else:
    print(f"fail：{response.status_code}")

Mag = []
Depth = []
for a in earthquake_data:
    Mag.append(a[2])
    Depth.append(a[3])

xray = [a for a in range(len(Mag))]

fig, ax = plt.subplots(2,1)
fig.suptitle('Magnitude vs Depth')

ax[0].plot(xray, Mag)
ax[0].set_ylabel('Magnitude',loc = 'top')
ax[1].plot(xray, Depth,color='red')
ax[1].set_ylabel('Depth',loc = 'top')

plt.show()