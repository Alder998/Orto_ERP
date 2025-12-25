import streamlit as st
from datetime import date
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")
st.title("I tuoi Acquisti 💰")
st.subheader("Aggiorna la tua contabilità")

# id_activity	Data	Attività	Prodotto	Peso	Prezzo	Note
df = excel.ExcelDataService().getExcelData(fileType="acquisti")[["id_activity","Data","Attività","Prodotto","Peso","Prezzo","Note"]]

data = st.date_input("Data",value=date.today())
att = st.selectbox(label = "Attività", options=["Zappare ⛏️", "Concimare 💩", "Paciamatura 👻",
                                                "Trattamenti 🧪", "Protezioni e reti 🔰", "Taglio erba 🚜",
                                                "Seminare 🫘","Piantare 🌱"])

# Initialize all objects
prod = None
peso = None
prezzo = None
prod_chimico = None

# populate variables
if (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].dropna().unique(), accept_new_options=True)
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")

prezzo = st.number_input("Prezzo (€)", min_value=0.0, step=0.1, format="%.2f")
note = st.text_area("Note", height=50)

if st.button("💾 Salva"):
    dati = {
        "Data": data,
        "Attività": att,
        "Prodotto": prod,
        "Peso": peso,
        "Prezzo": prezzo,
        "Prodotto chimico": prod_chimico,
        "Note": note,
    }
    try:
        excel.ExcelDataService().updateExcelData(dati, fileType="acquisti")
        st.success("Dati salvati correttamente nel dataset acquisti ✅")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")


st.subheader("\nI tuoi acquisti")
st.dataframe(df, width='stretch')
