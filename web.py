import streamlit as st
import pandas as pd
import plotly.express as px
import os 



st.set_page_config("Stránka", layout="wide")

#----------------- Data ---------------------#
data = pd.read_csv('zdrojak_raw.csv')
radky = ["idhod", "hodnota", "sldb_rok", "sldb_datum", "ukaz_txt", "misto_regpobytu_txt", "pohlavi_txt", "uzemi_txt", "uzemi_typ"]
data = data[radky]
data = data[data['uzemi_typ'] == 'obec']
data.to_csv('zdrojak.csv', index=False)

#px.bar(data, data["sldb_datum"], data["hodnota"])

#----------------- Sidebar ------------------#
sidebar = st.sidebar
sidebar.title(":bar_chart: :blue[Filtry]")
sidebar.caption("Vyberte potřebné filtry pro Vaši práci")


filter1 = sidebar.multiselect("Obec", data["uzemi_txt"].unique())

if filter1:
    data_2 = data[data["uzemi_typ"].isin(filter1)]
else:
    data_2 = data.copy()

filter2 = sidebar.

"""if not filter1 and not filter2:
    filtered_data = data
elif not filter2 and filter1:
    filtered_data = data_2
elif not filter1 and filter2:
    filtered_data = data_3
elif filter1 and filter2:
    data = data_3
#filter2 = sidebar.multiselect()"""

#------------------ Stránka ----------------#

#folium map. funkce pro python
st.write(px.bar(data, data["sldb_datum"], data["hodnota"]))







