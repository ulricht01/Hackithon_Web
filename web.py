import streamlit as st
import pandas as pd
import plotly.express as px
import os 
import math
import time



st.set_page_config("Stránka", layout="wide")

#----------------- Sčítání lidu ---------------------#
data = pd.read_csv('zdrojak_raw.csv')
souradnice = pd.read_csv('souradnice.csv')
data = data.merge(souradnice[['Obec', 'Okres', 'Kraj', 'Latitude', 'Longitude']], left_on='uzemi_txt', right_on='Obec', how='left')
radky = ["idhod", "hodnota", "sldb_rok", "sldb_datum", "ukaz_txt", "misto_regpobytu_txt", "pohlavi_txt", "uzemi_txt", "uzemi_typ", 'Okres', 'Kraj', 'Latitude', 'Longitude']
data = data[radky]
data = data[data['uzemi_typ'] == 'obec']
data["sldb_datum"] = pd.to_datetime(data["sldb_datum"]) 
data["sldb_datum"] = data["sldb_datum"].dt.strftime('%d.%m.%Y')
data.rename(columns={"uzemi_txt": "mesto"}, inplace=True)

data.to_csv('zdrojak.csv', index=False)

#------------------ Oral ---------------------------#

oral = pd.read_csv('oral.csv')
pohlavi_kraje = oral.groupby(['Kraj', 'Pohlaví']).size().unstack(fill_value=0)

#------------------ Cizinci ---------------------------#

cizinci = pd.read_csv('cizinci.csv')
cizinci_radky = ["hodnota","rok","kraj_txt","stobcan_txt"]
cizinci = cizinci[cizinci_radky]
cizinci_kraje = cizinci.groupby(['kraj_txt', 'stobcan_txt']).size().unstack(fill_value=0)
#px.bar(data, data["sldb_datum"], data["hodnota"])

#----------------- Sidebar ------------------#
sidebar = st.sidebar
sidebar.title(":bar_chart: :blue[Filtry]")
sidebar.caption("Vyberte potřebné filtry pro Vaši práci")


#filter1 = sidebar.multiselect("Kraj", data["Kraj"].unique())
filter1 = sidebar.multiselect("Sloupec pro filtrování", data.columns)

if filter1:
    data_2 = data[data["Kraj"].isin(filter1)]
else:
    data_2 = data.copy()

filter2 = sidebar.multiselect("Okres", data_2["Okres"].unique())

if filter2:
    data_3 = data_2[data_2["Okres"].isin(filter2)]
else:
    data_3 = data_2.copy()

filter3 = sidebar.multiselect("Obec", data_3["mesto"].unique())

if filter3:
    data_4 = data_3[data_3["mesto"].isin(filter3)]
else:
    data_4 = data_3.copy()


if not filter1 and not filter2 and not filter3:
    filtered_data = data
elif not filter2 and filter1:
    filtered_data = data_2
elif not filter1 and filter2:
    filtered_data = data_3
elif filter1 and filter2:
    filtered_data = data_4
    

#------------------ Stránka ----------------#
datum = filtered_data["sldb_datum"].max()
st.subheader(f"Datum sčítání: {datum}")

#------------------ Graf zobrazení početu obyvatel 
expander_1 = st.expander("Počet lidí :bar_chart:")
with expander_1:
    st.bar_chart(filtered_data, x= "Kraj", y= "hodnota")
    st.bar_chart(filtered_data, x= "Okres", y= "hodnota")
    st.bar_chart(filtered_data, x= "mesto", y= "hodnota")

expander_2 = st.expander("Počet lidí :world_map:")
with expander_2:
    filtered_data['bod_velikost'] = filtered_data['hodnota']# / (math.log10(filtered_data['hodnota']) + 1) * 2
    st.map(filtered_data.dropna(subset=['bod_velikost', 'Latitude', 'Longitude']), 
           latitude='Latitude', 
           longitude='Longitude', 
           size = 'bod_velikost',
           color = '#0044ff')

expander_3 = st.expander("Oral :blush:")
with expander_3:
    st.bar_chart(pohlavi_kraje)

expander_4 = st.expander("Cizinci")
with expander_4:
    st.bar_chart(cizinci_kraje)
    



