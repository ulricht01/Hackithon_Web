import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config("Stránka")

#----------------- Data ---------------------#
data = pd.read_csv('zdrojak.csv')
radky = ["idhod", "hodnota", "sldb_rok", "sldb_datum", "ukaz_txt", "misto_regpobytu_txt", "pohlavi_txt", "uzemi_txt", "uzemi_typ"]
data = data[radky]

#px.bar(data, data["sldb_datum"], data["hodnota"])

#----------------- Sidebar ------------------#
sidebar = st.sidebar
sidebar.title(":bar_chart: :blue[Filtry]")
sidebar.caption("Vyberte potřebné filtry pro Vaši práci")

filter1 = sidebar.multiselect("Obec", data["uzemi_typ"].unique())

if filter1:
    data_2 = data[data["uzemi_typ"].isin(filter1)]
else:
    data_2 = data.copy()

filter2 = sidebar.multiselect("xxxx", data_2["uzemi_txt"].unique())

if filter2:
    data_3 = data_2[data_2["uzemi_typ"].isin(filter2)]
else:
    data_3 = data_2.copy()

if not filter1 and not filter2:
    filtered_data = data
elif not filter2 and filter1:
    filtered_data = data_2
elif not filter1 and filter2:
    filtered_data = data_3
elif filter1 and filter2:
    data = data_3
#filter2 = sidebar.multiselect()

#------------------ Stránka ----------------#

#st.table(data)
#folium map. funkce pro python
st.write(px.bar(data, data["sldb_datum"], data["hodnota"]))





