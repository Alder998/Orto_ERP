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
att = st.selectbox(label = "Attività", options=["Preparazione Terreno ⛏️", "Irrigazione 💦", "Rincalzatura 🚜",
                                                "Trattamenti 🧪", "Raccogliere 🍎",
                                                "Seminare 🫘","Piantare 🌱"])

# Initialize
# 0. Activities to preparate the field
settore = None
mq = None
tempo = None

prod = None
quantita = None
peso = None
prezzo = None
prod_chimico = None
acqua_utilizzata = None

# populate variables
if att == "Preparazione Terreno ⛏️":
    #prod_chimico = st.selectbox(label = "Prodotto chimico utilizzato", options=df[df["Attività"]=="Concimare"]["Prodotto chimico"].dropna().unique(), accept_new_options=True)
    settore = st.number_input("Settore Orto (numero)", min_value=0, step=1)
    mq = st.number_input("Metri Quadri (m2)", min_value=0, step=5)
    tempo = st.number_input("Tempo impiegato (ore)", min_value=0.0, step=0.1, format="%.1f")
    att1 = st.selectbox(label = "Zappare", options=["No", "Si"], accept_new_options=False)
    att2 = st.selectbox(label = "Concimare", options=["No", "Si"], accept_new_options=False)
    att3 = st.selectbox(label = "Paciamatura", options=["No", "Si"], accept_new_options=False)
    att4 = st.selectbox(label = "Protezione e reti", options=["No", "Si"], accept_new_options=False)
    att5 = st.selectbox(label = "Taglio Erba", options=["No", "Si"], accept_new_options=False)

elif (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    settore = st.number_input("Settore Orto (numero)", min_value=0, step=1)
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].dropna().unique(), accept_new_options=True)
    quantita = st.number_input("Quantità (pz)", min_value=0, step=1)
elif att == "Raccogliere 🍎":
    settore = st.number_input("Settore Orto (numero)", min_value=0, step=1)
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].dropna().unique(), accept_new_options=True)
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")
elif att == "Trattamenti 🧪":
    settore = st.number_input("Settore Orto (numero)", min_value=0, step=1)
    prod_chimico = st.selectbox(label = "Prodotto chimico utilizzato", options=df[df["Attività"]=="Trattamenti"]["Prodotto chimico"].dropna().unique(), accept_new_options=True)
    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].unique(), accept_new_options=True)
    tempo = st.number_input("Tempo impiegato (ore)", min_value=0.0, step=0.1, format="%.1f")
    #prezzo = st.number_input("Prezzo (€) del trattamento", min_value=0.0, step=0.1, format="%.2f")
elif att == "Rincalzatura 🚜":
    settore = st.number_input("Settore Orto (numero)", min_value=0, step=1)
    tempo = st.number_input("Tempo impiegato (ore)", min_value=0.0, step=0.1, format="%.1f")

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
        "Acqua utilizzata": acqua_utilizzata,
        "Tempo atmosferico": tempo,
        "Note": note,
    }
    try:
        excel.ExcelDataService().updateExcelData(dati)
        st.success("Dati salvati correttamente ✅")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")
