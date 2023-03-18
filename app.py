import numpy as np
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static

st.title("The Chernobyl Disaster Air Concentration Dashboard")

def clean_data(data):
    m = data['I_131_(Bq/m3)'].str.contains('L|\?', regex=True, na=False)
    data.loc[m,'I_131_(Bq/m3)'] = None

    m = data['Cs_134_(Bq/m3)'].str.contains('N|\?', regex=True)
    data.loc[m,'Cs_134_(Bq/m3)'] = None

    m = data['Cs_137_(Bq/m3)'].str.contains('N|\?', regex=True)
    data.loc[m,'Cs_137_(Bq/m3)'] = None

    data['Date'] = pd.to_datetime(data['Date'], format='%y/%m/%d')
    data['I_131_(Bq/m3)'] = pd.to_numeric(data['I_131_(Bq/m3)'])
    data['Cs_134_(Bq/m3)'] = pd.to_numeric(data['Cs_134_(Bq/m3)'])
    data['Cs_137_(Bq/m3)'] = pd.to_numeric(data['Cs_137_(Bq/m3)'])
    
    data.dropna(inplace = True)
    
    return data

data = pd.read_csv("data.csv")

df = clean_data(data)

df_sorted = df.sort_values(by='Cs_137_(Bq/m3)', ascending=False)

col1, col2 = st.columns(2)

with col1:
   st.subheader("Most Polluted City")
   st.text(df_sorted.iloc[0]['Ville'])
   st.write("Cesium-137  = ", df_sorted.iloc[0]['Cs_137_(Bq/m3)'])
   
with col2:
   st.subheader("Least Polluted City")
   st.text(df_sorted.iloc[-1]['Ville'])
   st.write("Cesium-137  = ", df_sorted.iloc[-1]['Cs_137_(Bq/m3)'])
   
st.write(" ")

st.subheader("Find concentration of specific city")

option = st.selectbox(
    'Choose City',
    ('RISOE', 'AACHEN(RWTH)', 'ANSBACH', 'BERLIN-WEST', 
     'BROTJACKLRIEGEL', 'FREIBURG(BZS)', 'FREIBURG(DWD)', 
     'GOETTINGEN', 'HANNOVER', 'KARLSRUHE', 'MEINERZHAGEN', 
     'NEUHERBERG', 'NORDERNEY', 'OFFENBACH', 'ROTTENBURG', 
     'STARNBERG', 'WALDHOF', 'CADARACHE', 'CHINON', 'CHOOZ',
     'CRUAS', 'FESSENHEIM', 'FLAMANVILLE', 'GRAVELINES', 
     'GRENOBLE', 'MARCOULE', 'MONACO', 'ORSAY', 'PARIS', 
     'SACLAY', 'TRICASTIN', 'VERDUN', 'BOLOGNA', 'BRASIMONE', 
     'CAPANNA', 'CASACCIA', 'ISPRA', 'SALUGGIA(eurex)', 
     'SALUGGIA(IFEC)', 'TRISAIA', 'BILTHOVEN', 'DELFT', 
     'EELDE', 'GRONINGEN', 'PETTEN', 'VLISSINGEN', 'ATTIKIS', 
     'KOZANIS', 'THESSALONIKI', 'BERKELEY', 'CHAPELCROSS', 
     'GLASGOW', 'HARWELL', 'BRUXELLES(Ixelles)', 'MOL', 
     'TARRAGONA', 'VALENCIA', 'FRIBOURG', 'SPIEZ', 'BREGENZ',
     'GRAZ', 'INNSBRUCK', 'KLAGENFURT', 'LINZ', 'SALZBURG',
     'KONALA(Helsinki)NW', 'NURMIJAERVI', 'BERGEN', 'KJELLER',
     'OSLO', 'VAERNES', 'GOETEBORG', 'LJUNGBYHED', 'OESTERSUND', 
     'STOCKHOLM', 'UMEAA', 'BRATISLAVA', 'CESKE', 'JASLOVSKE', 'KOSICE', 'BUDAPEST'))

if option:
    city_data = df.loc[df['Ville'] == option]

    # Extract the concentration values for Iodine, Cs_134 and Cs_137
    iodine_concentration = city_data['I_131_(Bq/m3)'].values[0]
    cs_134_concentration = city_data['Cs_134_(Bq/m3)'].values[0]
    cs_137_concentration = city_data['Cs_137_(Bq/m3)'].values[0]

    # Print the concentration values
    st.write(f"The concentration of Iodine in {option} is {iodine_concentration} Bq/m3")
    st.write(f"The concentration of Cs_134 in {option} is {cs_134_concentration} Bq/m3")
    st.write(f"The concentration of Cs_137 in {option} is {cs_137_concentration} Bq/m3")

map_button = st.button("SHOW MAP", use_container_width = True)

if map_button:
    
    map = folium.Map(location=[df['Y'].mean(), df['X'].mean()], zoom_start=5)

    for index, row in df.iterrows():
        location = [row['Y'], row['X']]
        popup = f"<b>{row['Ville']}</b><br>" \
                f"I-131: {row['I_131_(Bq/m3)']} Bq/m3<br>" \
                f"Cs-134: {row['Cs_134_(Bq/m3)']} Bq/m3<br>" \
                f"Cs-137: {row['Cs_137_(Bq/m3)']} Bq/m3<br>" \
                f"Sampling duration: {row['Duration(h.min)']} hours"
        marker = folium.Marker(location=location, popup=popup, tooltip=row['PAYS'])
        marker.add_to(map)

    # display the map in Streamlit
    folium_static(map)
    

st.write("")
st.caption("Acknowledgements : CEC Joint Research Centre Ispra, JOINT RESEARCH CENTRE Directorate for Nuclear Safety and Security.")
