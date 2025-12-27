import streamlit as st
from datetime import date
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")
st.title("I tuoi Acquisti 💰")
st.subheader("Aggiorna la tua contabilità")

# id_activity	Data	Attività	Prodotto	Peso	Prezzo	Note
df = excel.ExcelDataService(fileType="acquisti").getExcelData()
df_produzione = excel.ExcelDataService(fileType="produzione").getExcelData()

data = st.date_input("Data",value=date.today())
fornitore = st.text_input("Fornitore")

st.divider()

# Initialize all objects
#prod = None
#peso = None
#prezzo = None
#prod_chimico = None

# populate variables
#if (att == "Seminare 🫘") | (att == "Piantare 🌱"):
#    prod = st.selectbox(label = "Prodotto", options=df["Prodotto"].dropna().unique(), accept_new_options=True)
#    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")

#prezzo = st.number_input("Prezzo (€)", min_value=0.0, step=0.1, format="%.2f")
#note = st.text_area("Note", height=50)
#
#if st.button("💾 Salva"):
#    dati = {
#        "Data": data,
#        "Attività": att,
#        "Prodotto": prod,
#        "Peso": peso,
#        "Prezzo": prezzo,
#        "Prodotto chimico": prod_chimico,
#        "Note": note,
#    }
#    try:
#        excel.ExcelDataService(fileType="acquisti").updateExcelData(dati)
#        st.success("Dati salvati correttamente nel dataset acquisti ✅")
#    except Exception as e:
#        st.error(f"Errore durante il salvataggio: {e}")

# Initialize session state
if "rows" not in st.session_state:
    st.session_state.rows = [
        {"Attività": "", "Note": "", "Prezzo": "", "Prodotto": "", "Quantita": ""}
    ]

# Add Botton
if st.button("➕ Aggiungi Acquisto"):
    st.session_state.rows.append(
        {"Attività": "", "Note": "", "Prezzo": "", "Prodotto": "", "Quantita": ""}
    )

for i, row in enumerate(st.session_state.rows):
    att, note, prezzo, prod, quant = st.columns(5)

    with att:
        row["Attività"] = st.selectbox(label = f"Attività legata all'acquisto {i+1}", options=["Preparazione Terreno ⛏️",
                                                "Rincalzatura 🚜", "Trattamenti 🧪", "Seminare 🫘", "Piantare 🌱"])
    with note:
        row["Note"] = st.text_input(f"Note acquisto {i+1}")

    with prezzo:
        row["Prezzo"] = st.number_input(f"Prezzo (€) {i+1}", min_value=0.0, step=0.1, format="%.2f")

    with prod:
        if (row["Attività"] == "Seminare 🫘") | (row["Attività"] == "Piantare 🌱"):
            row["Prodotto"] = st.selectbox(label=f"Prodotto {i+1}", options=df_produzione["Prodotto"].dropna().unique(), accept_new_options=True)
    with quant:
        if (row["Attività"] == "Seminare 🫘") | (row["Attività"] == "Piantare 🌱"):
            row["Quantita"] = st.number_input(f"Quantità (pz) {i+1}", min_value=0, step=1)

    # remove row
    if st.button(f"❌ Rimuovi Acquisto {i + 1}"):
        st.session_state.rows.pop(i)
        st.rerun()