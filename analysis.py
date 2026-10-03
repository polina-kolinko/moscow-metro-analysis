import pandas as pd
import matplotlib.pyplot as plt
import folium

passenger_flow = pd.read_csv('data/passenger_flow.csv', sep=';')
passenger_flow = passenger_flow.drop(columns='Unnamed: 7')
passenger_flow = passenger_flow.drop(index=0)
passenger_flow = passenger_flow.reset_index(drop=True)

passenger_flow['Year'] = pd.to_numeric(passenger_flow['Year'])
passenger_flow['Incoming passengers'] = pd.to_numeric(passenger_flow['Incoming passengers'])
passenger_flow['Outgoing passengers'] = pd.to_numeric(passenger_flow['Outgoing passengers'])



metro_entrances = pd.read_csv('data/metro_entrances.csv', sep=';')
metro_entrances = metro_entrances.drop(columns='Unnamed: 23')
metro_entrances = metro_entrances.drop(index=0)
metro_entrances = metro_entrances.reset_index(drop=True)
metro_entrances['Longitude in WGS-84'] = pd.to_numeric(metro_entrances['Longitude in WGS-84'])
metro_entrances['Latitude in WGS-84'] = pd.to_numeric(metro_entrances['Latitude in WGS-84'])


station_coordinates = metro_entrances.groupby(['Metro station name', 'Line name']).agg(Средняя_долгота= ('Longitude in WGS-84','mean'), Средняя_широта=('Latitude in WGS-84','mean')).reset_index()
metro_data = passenger_flow.merge(station_coordinates, on=['Metro station name','Line name'], how='left')
unmatched = metro_data[metro_data['Средняя_долгота'].isna()]
unmatched = unmatched[['Metro station name','Line name']].drop_duplicates()


flow_2025 = passenger_flow[passenger_flow['Year'] == 2025].copy()
flow_2025['Total passengers'] = flow_2025['Incoming passengers'] + flow_2025['Outgoing passengers']
station_flow_2025 = flow_2025.groupby(['Metro station name', 'Line name'])['Total passengers'].sum().reset_index()
top_10_2025 = station_flow_2025.sort_values(by='Total passengers',ascending=False).head(10)
quarters_count_2025 = flow_2025.groupby(['Metro station name', 'Line name']).size()
#print(quarters_count_2025[quarters_count_2025 < 4])
#print(station_flow_2025[station_flow_2025['Total passengers'] == 0])
full_year_stations = quarters_count_2025[quarters_count_2025 == 4].reset_index()
full_year_flow_2025 = full_year_stations.merge(station_flow_2025, on=['Metro station name','Line name'], how='left')
nonzero_full_year_flow_2025 = full_year_flow_2025[full_year_flow_2025['Total passengers'] > 0]
bottom_10_2025 = nonzero_full_year_flow_2025.sort_values(by='Total passengers',ascending=True).head(10)
line_flow_2025 = flow_2025.groupby(['Line name'])['Total passengers'].sum().reset_index()
avg_station_flow_by_line_2025 = nonzero_full_year_flow_2025.groupby(['Line name'])['Total passengers'].mean().reset_index()


passenger_flow['Total passengers'] = passenger_flow['Incoming passengers'] + passenger_flow['Outgoing passengers']
quarterly_flow = passenger_flow.groupby(['Year', 'Quarter'])['Total passengers'].sum().reset_index()
quarterly_flow['Period'] = quarterly_flow['Year'].astype(str) + ' ' + quarterly_flow['Quarter'].astype(str)


x = quarterly_flow['Period']
y = quarterly_flow['Total passengers'] / 1_000_000
plt.figure(figsize=(12, 6))
plt.plot(x, y)
plt.xticks(rotation=45)
plt.tight_layout()
plt.title('Динамика пассажиропотока Московского метро по кварталам')
plt.xlabel('период')
plt.ylabel('общий пассажиропоток, млн')
plt.savefig("images/quarterly_passenger_flow.png")
plt.close()
#plt.show()

full_years_flow = quarterly_flow[quarterly_flow['Year'] <= 2025]
full_years_flow = full_years_flow.groupby(['Quarter'])['Total passengers'].mean()

x = top_10_2025['Metro station name']
y = top_10_2025['Total passengers'] / 1_000_000
plt.figure(figsize=(12, 6))
plt.barh(x, y)
plt.gca().invert_yaxis()
plt.title('Топ-10 станций по пассажиропотоку в 2025 году')
plt.xlabel('Пассажиропоток, млн')
plt.tight_layout()
plt.savefig("images/top_10_stations_2025.png")
plt.close()
#plt.show()

avg_station_flow_by_line_2025 = avg_station_flow_by_line_2025.sort_values(by='Total passengers',ascending=False)
x = avg_station_flow_by_line_2025['Line name']
y = avg_station_flow_by_line_2025['Total passengers'] / 1_000_000
plt.figure(figsize=(12, 6))
plt.barh(x, y)
plt.gca().invert_yaxis()
plt.title('Средний пассажиропоток на станцию по линиям метро, 2025')
plt.xlabel('Пассажиропоток, млн')
plt.tight_layout()
plt.savefig("images/avg_station_flow_by_line_2025.png")
plt.close()
#plt.show()

metro_map = folium.Map(location=[55.75, 37.62],zoom_start=10)

map_data = station_flow_2025.merge(station_coordinates, on=['Metro station name','Line name'], how='left')
#print(map_data[['Средняя_широта','Средняя_долгота']].isna().sum())
missing_coordinates = map_data[map_data['Средняя_широта'].isna()]
#print(missing_coordinates)
map_data_clean = map_data.dropna(subset=['Средняя_широта', 'Средняя_долгота'])
map_data_plot = map_data_clean[map_data_clean['Total passengers'] > 0]


for index, row in map_data_plot.iterrows():
    radius = 3 + row['Total passengers'] / 3_000_000

    popup_text = (
        f"Станция: {row['Metro station name']}<br>"
        f"Линия: {row['Line name']}<br>"
        f"Пассажиропоток: {row['Total passengers']}"
    )

    folium.CircleMarker(
        location=[row['Средняя_широта'], row['Средняя_долгота']],
        radius=radius,
        popup=popup_text,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(metro_map)

metro_map.save("metro_map.html")
