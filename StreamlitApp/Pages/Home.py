import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")

st.title("Ciao Guido 🌱")
st.subheader("I tuoi dati e le tue attività")

st.subheader("\nLa tua ultima attività")
data = excel.ExcelDataService().getExcelData()[["Data","Attività","Prodotto","Quantità","Peso","Tempo atmosferico","Note"]]
data_last = data[data["Data"] == data["Data"].max()].reset_index(drop=True)
st.dataframe(data_last, width='stretch')
