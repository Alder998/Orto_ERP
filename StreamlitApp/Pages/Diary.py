import streamlit as st
from datetime import date
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")
st.title("Il tuo diario 🖊️")
st.subheader("Aggiungi le tue attività")

# Load data for options
df = excel.ExcelDataService().getExcelData()[["id_activity", "Data","Attività","Prodotto","Quantità","Peso", "Prodotto chimico","Tempo atmosferico","Note"]]

# Add all the selectBox

data = st.date_input("Data",value=date.today())
att = st.selectbox(label = "Attività", options=["Zappare ⛏️", "Concimare 💩", "Paciamatura 👻", "Irrigazione 💦",
                                                "Trattamenti 🧪", "Protezioni e reti 🔰", "Taglio erba 🚜", "Raccogliere 🍎",
                                                "Seminare 🫘","Piantare 🌱"])

# Initialize
prod = None
quantita = None
peso = None
prezzo = None
prod_chimico = None

# populate variables
if (att == "Raccogliere 🍎") | (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].unique(), accept_new_options=True)
    quantita = st.number_input("Quantità (pz)", min_value=0, step=1)
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")
    prezzo = st.number_input("Prezzo (€)", min_value=0.0, step=0.1, format="%.2f")
elif att == "Concimare 💩":
    prod_chimico = st.selectbox(label = "Prodotto chimico utilizzato", options=df["Prodotto chimico"].unique(), accept_new_options=True)
elif att == "Trattamenti 🧪":
    prod_chimico = st.selectbox(label = "Prodotto chimico utilizzato", options=df["Prodotto chimico"].unique(), accept_new_options=True)
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].unique(), accept_new_options=True)
    prezzo = st.number_input("Prezzo (€) del trattamento", min_value=0.0, step=0.1, format="%.2f")

tempo = st.selectbox(label = "Tempo Atmosferico", options=["Sereno", "nuvole sparse", "nuvoloso", "pioggia"])
note = st.text_area("Note", height=50)

# Save module
if st.button("💾 Salva"):
    dati = {
        "Data": data,
        "Attività": att,
        "Prodotto": prod,
        "Quantità": quantita,
        "Peso": peso,
        "Prezzo": prezzo,
        "Prodotto chimico": prod_chimico,
        "Tempo atmosferico": tempo,
        "Note": note,
    }
    try:
        excel.ExcelDataService().updateExcelData(dati)
        st.success("Dati salvati correttamente ✅")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")
