import streamlit as st
from datetime import date
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")
st.title("Il tuo Terrario 🐸")
st.subheader("Aggiungi le tue attività di coltivazione indoor")

# Load data for options
df_att = excel.ExcelDataService(fileType="attivita").getExcelData()
df_produzione = excel.ExcelDataService(fileType="produzione").getExcelData()

# Add all the selectBox
data = st.date_input("Data",value=date.today())
att = st.selectbox(label = "Attività", options=["Seminare 🫘","Germinazione 🌼"])

# Initialize
# populate variables
tempo_imp = st.number_input("Tempo impiegato (ore)", min_value=0.0, step=0.1, format="%.1f")
prod = st.selectbox(label = "Prodotto", options=df_produzione["Prodotto"].dropna().unique(), accept_new_options=True)
note = st.text_area("Note", height=50)

# Save module
if st.button("💾 Salva"):
    dati = {
        "Data": data,
        "Attività": att,
        "Prodotto": prod,
        "tempo impiegato": tempo_imp,
        "Note": note,
    }
    try:
        excel.ExcelDataService(fileType="terrario").updateExcelData(dati)
        st.success("Dati salvati correttamente nel dataset terrario ✅")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")
