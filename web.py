import streamlit as st
import pandas as pd
import plotly.express as px
import os 
import time



st.set_page_config("Stránka", layout="wide")

#----------------- Data ---------------------#
data = pd.read_csv('zdrojak_raw.csv')
souradnice = pd.read_csv('souradnice.csv')
# Přidání sloupců Latitude a Longitude na základě názvu obce
data = data.merge(souradnice[['Obec', 'Okres', 'Kraj', 'Latitude', 'Longitude']], left_on='uzemi_txt', right_on='Obec', how='left')

radky = ["idhod", "hodnota", "sldb_rok", "sldb_datum", "ukaz_txt", "misto_regpobytu_txt", "pohlavi_txt", "uzemi_txt", "uzemi_typ", 'Okres', 'Kraj', 'Latitude', 'Longitude']
data = data[radky]
data = data[data['uzemi_typ'] == 'obec']
data["sldb_datum"] = pd.to_datetime(data["sldb_datum"]) 
data["sldb_datum"] = data["sldb_datum"].dt.strftime('%d.%m.%Y')
#Přidat souřadnice

data.to_csv('zdrojak.csv', index=False)

#px.bar(data, data["sldb_datum"], data["hodnota"])

#----------------- Sidebar ------------------#
sidebar = st.sidebar
sidebar.title(":bar_chart: :blue[Filtry]")
sidebar.caption("Vyberte potřebné filtry pro Vaši práci")


filter1 = sidebar.multiselect("Kraj", data["Kraj"].unique())

if filter1:
    data_2 = data[data["Kraj"].isin(filter1)]
else:
    data_2 = data.copy()

filter2 = sidebar.multiselect("Okres", data_2["Okres"].unique())

if filter2:
    data_3 = data_2[data_2["Okres"].isin(filter2)]
else:
    data_3 = data_2.copy()

filter3 = sidebar.multiselect("Obec", data_3["uzemi_txt"].unique())

if filter3:
    data_4 = data_3[data_3["uzemi_typ"].isin(filter3)]
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
expander_1 = st.expander("Počet lidí")
with expander_1:
    st.bar_chart(filtered_data, x= "Kraj", y= "hodnota")
    st.bar_chart(filtered_data, x= "Okres", y= "hodnota")
    st.bar_chart(filtered_data, x= "uzemi_txt", y= "hodnota")

expander_2 = st.expander("Počet lidí dle okresů")
with expander_2:
    pass
    



