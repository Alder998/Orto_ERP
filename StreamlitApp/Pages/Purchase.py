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
att = None
note = None
prezzo = None
prod = None
quant = None

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

multiple_rows = []
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

    # Append Rows to the list
    multiple_rows.append(row)
    # remove row
    if st.button(f"❌ Rimuovi Acquisto {i + 1}"):
        st.session_state.rows.pop(i)
        st.rerun()

# Save module
if st.button("💾 Salva Tutti gli acquisti"):
    for i, srow in enumerate(multiple_rows):
        dati = {
            "Data": data,
            "Attività": srow["Attività"],
            "Fornitore": fornitore,
            "Prodotto": srow["Prodotto"],
            "Quantità": srow["Quantita"],
            "Prezzo": srow["Prezzo"],
            "Note": srow["Note"],
        }
        try:
            excel.ExcelDataService(fileType="acquisti").updateExcelData(dati)
            if i == 0:
                st.success("Tutti i dati salvati correttamente nel dataset acquisti ✅")
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")