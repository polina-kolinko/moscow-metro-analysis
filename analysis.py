import pandas as pd
import matplotlib.pyplot as plt

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

#print(passenger_flow[passenger_flow['Metro station name'] == 'Шелепиха'])
#print(metro_entrances[['Metro station name','Line name','Name']][metro_entrances['Metro station name'] == 'Шелепиха'])
#print(passenger_flow[passenger_flow['Metro station name'] == 'Деловой центр'])
#print(metro_entrances[['Metro station name','Line name','Name']][metro_entrances['Metro station name'] == 'Деловой центр'])

#print(metro_entrances.head())
#print(metro_entrances.shape)
#print(metro_entrances.dtypes)
#print(metro_entrances[['Name', 'Metro station name', 'Line name', 'Number of exit', 'Longitude in WGS-84', 'Latitude in WGS-84']].head(10))
#print(metro_entrances.groupby(['Metro station name', 'Line name']).size())

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


#x = quarterly_flow['Period']
#y = quarterly_flow['Total passengers']
#plt.figure(figsize=(12, 6))
#lt.plot(x, y)
#plt.xticks(rotation=45)
#plt.tight_layout()
#plt.title('Динамика пассажиропотока Московского метро по кварталам')
#plt.xlabel('период')
#plt.ylabel('общий пассажиропоток')
#plt.show()

full_years_flow = quarterly_flow[quarterly_flow['Year'] <= 2025]
full_years_flow = full_years_flow.groupby(['Quarter'])['Total passengers'].mean()
print(full_years_flow)