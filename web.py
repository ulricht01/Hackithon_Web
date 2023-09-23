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
data = data.dropna(subset=['Kraj'])
data = data.dropna(subset=['Okres'])

data.to_csv('zdrojak.csv', index=False)

#------------------ Oral ---------------------------#

oral = pd.read_csv('oral.csv')
pohlavi_kraje = oral.groupby(['Kraj', 'Pohlaví']).size().unstack(fill_value=0)
pohledy = oral.groupby(['Pohlaví', "Praktikujete orální sex?"]).size().unstack(fill_value=0)

#------------------ Cizinci ---------------------------#

cizinci = pd.read_csv('cizinci.csv')
cizinci_radky = ["hodnota","rok","kraj_txt","stobcan_txt", "vek_txt", "pohlavi_txt"]
cizinci = cizinci[cizinci_radky]
cizinci = cizinci.dropna(subset=['kraj_txt'])
cizinci = cizinci.dropna(subset=['stobcan_txt'])
cizinci = cizinci.dropna(subset=['vek_txt'])
cizinci = cizinci.dropna(subset=['pohlavi_txt'])

#----------------- Sidebar ------------------#
sidebar = st.sidebar
sidebar.title("📊 :blue[Filtry]")
sidebar.caption("Vyberte potřebné filtry pro Vaši práci")


filter1 = sidebar.multiselect("Kraj", data["Kraj"].unique())
#filter1 = sidebar.multiselect("Sloupec pro filtrování", data.columns)

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
    

datasets = {
    "Dataset 1": cizinci,
    "Dataset 2": oral,
    "Dataset 3": data
}

#------------------ Stránka ----------------#
datum = filtered_data["sldb_datum"].max()
st.subheader(f"Datum sčítání: {datum}")

#------------------ Graf zobrazení početu obyvatel 


expander_1 = st.expander("Počet lidí 📊")
with expander_1:
        st.bar_chart(filtered_data, x= "Kraj", y= "hodnota")
        st.bar_chart(filtered_data, x= "Okres", y= "hodnota")
        st.bar_chart(filtered_data, x= "mesto", y= "hodnota")
    

expander_2 = st.expander("Počet lidí 🗺️")
with expander_2:
    filtered_data['bod_velikost'] = filtered_data['hodnota'] / 10  #[list(map(int, row)) for row in arr]
    st.map(filtered_data.dropna(subset=['bod_velikost', 'Latitude', 'Longitude']), 
           latitude='Latitude', 
           longitude='Longitude', 
           size = 'bod_velikost')


oral1 = oral.copy()

expander_3 = st.expander("Oral 😊")

with expander_3:
    filter_special1 = st.multiselect("Kraje-Oral", oral1["Kraj"].unique())
    if filter_special1:
        oral1 = oral1[oral1["Kraj"].isin(filter_special1)]
        pohlavi_kraje = oral1.groupby(['Kraj', 'Pohlaví']).size().unstack(fill_value=0)
    st.bar_chart(pohlavi_kraje)
    st.bar_chart(pohledy)

#Segregace menšin

filtered_data1 = cizinci.copy()
expander_4 = st.expander("Cizinci")

with expander_4:
    filter_special2 = st.multiselect("Věk_cizinec", filtered_data1["vek_txt"].unique())
    if filter_special2:
        filtered_data1 = filtered_data1[filtered_data1["vek_txt"].isin(filter_special2)]
    
    filter_special3 = st.multiselect("Pohlaví_cizinec", filtered_data1["pohlavi_txt"].unique())
    if filter_special3:
        filtered_data1 = filtered_data1[filtered_data1["pohlavi_txt"].isin(filter_special3)]
    
    filter_special4 = st.multiselect("Původ_cizinec", filtered_data1["stobcan_txt"].unique())
    if filter_special4:
        filtered_data1 = filtered_data1[filtered_data1["stobcan_txt"].isin(filter_special4)]
    
    filter_special5 = st.multiselect("Kraj_cizinec", filtered_data1["kraj_txt"].unique())
    if filter_special5:
        filtered_data1 = filtered_data1[filtered_data1["kraj_txt"].isin(filter_special5)]
        
    st.bar_chart(cizinci, x='kraj_txt', y='hodnota')
    st.bar_chart(cizinci, x='pohlavi_txt', y='hodnota')

expender_5 = st.expander("Víra")
with expender_5:
    pass#st.
#a