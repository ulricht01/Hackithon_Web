import streamlit as st
import pandas as pd
import plotly.express as px
from flask import Flask

st.set_page_config("Stránka")

app = Flask(__name__)

@app.route('/run_python_script')
def run_python_script():
    #----------------- Data ---------------------#
    data = pd.read_csv('zdrojak.csv', nrows=50)
    radky = ["idhod", "hodnota", "sldb_rok", "sldb_datum", "ukaz_txt", "misto_regpobytu_txt", "pohlavi_txt", "uzemi_txt", "uzemi_typ"]
    data = data[radky]

    #px.bar(data, data["sldb_datum"], data["hodnota"])

    #----------------- Sidebar ------------------#
    sidebar = st.sidebar
    sidebar.title(":bar_chart: :blue[Filtry]")
    sidebar.caption("Vyberte potřebné filtry pro Vaši práci")

    filter1 = sidebar.multiselect("Kraje", [])
    filter2 = sidebar.multiselect

    #------------------ Stránka ----------------#

    st.table(data)
    #folium map. funkce pro python
    st.write(px.bar(data, data["sldb_datum"], data["hodnota"]))





