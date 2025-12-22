import streamlit as st
from datetime import date
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")

st.title("Il tuo diario 🖊️")

st.subheader("Aggiungi le tue attività")

# Add all the selectBox

data = st.date_input(
    "Data",
    value=date.today()
)

att = st.text_input("Attività")
prod = st.text_input("Prodotto")
quantita = st.number_input("Quantità (pz)", min_value=0, step=1)
peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")
tempo = st.selectbox(label = "Tempo Atmosferico", options=["Sereno", "nuvole sparse", "nuvoloso", "pioggia"])
note = st.text_area("Note", height=50)

if st.button("💾 Salva"):
    dati = {
        "Data":data,
        "Attività":att,
        "Prodotto":prod,
        "Quantità":quantita,
        "Peso":peso,
        "Tempo atmosferico":tempo,
        "Note": note,
    }
    try:
        excel.ExcelDataService().updateExcelData(dati)
        st.success("Dati salvati correttamente ✅")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")