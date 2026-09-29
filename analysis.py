import pandas as pd

passenger_flow = pd.read_csv('data/passenger_flow.csv', sep=';')
passenger_flow = passenger_flow.drop(columns='Unnamed: 7')
passenger_flow = passenger_flow.drop(index=0)
passenger_flow = passenger_flow.reset_index(drop=True)

passenger_flow['Year'] = pd.to_numeric(passenger_flow['Year'])
passenger_flow['Incoming passengers'] = pd.to_numeric(passenger_flow['Incoming passengers'])
passenger_flow['Outgoing passengers'] = pd.to_numeric(passenger_flow['Outgoing passengers'])

#print(passenger_flow.head())
#print(passenger_flow.shape)
#print(passenger_flow.dtypes)
#print(passenger_flow.isna().sum())
#print(passenger_flow.duplicated().sum())
#print(passenger_flow['Year'].unique())
#print(passenger_flow['Quarter'].unique())
#print(passenger_flow.groupby(['Year', 'Quarter']).size())
print(passenger_flow.duplicated(subset=['Metro station name', 'Line name', 'Year', 'Quarter']).sum())