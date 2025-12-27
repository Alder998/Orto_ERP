import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel
import pandas as pd

st.set_page_config(layout="wide")

st.title("Il tuo Dataset 🧮")
st.subheader("Consulta i tuoi dati di produzione 🍎")

# Add dataset
data = excel.ExcelDataService(fileType="produzione").getExcelData()
data["Data"] = pd.to_datetime(data["Data"]).dt.strftime("%d/%m/%Y")
att = st.selectbox(label = "Seleziona una attività", options=["Trattamenti 🧪","Seminare 🫘","Piantare 🌱", "Raccogliere 🍎"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

if (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    data_filtered = data_filtered[["id_activity", "Data","Attività", "Settore Orto", "Prodotto","Quantità","Tempo atmosferico","Note"]]
elif (att == "Raccogliere 🍎"):
    data_filtered = data_filtered[["id_activity", "Data","Attività", "Settore Orto","Prodotto","Peso","Tempo atmosferico","Note"]]
elif (att == "Trattamenti 🧪"):
    data_filtered = data_filtered[["id_activity","Data","Attività", "Settore Orto","Prodotto","Prodotto chimico","Tempo atmosferico","Note"]]
else:
    data_filtered = data_filtered[["id_activity","Data","Attività", "Settore Orto","Tempo atmosferico","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}")

if st.button("❌ Elimina Produzione selezionata"):
    row_id = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService(fileType="produzione").deleteExcelRow(row_id)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")

# Add divider
st.divider()

# Activities data
st.subheader("Consulta i tuoi dati di Attività ⛏️")

# Add dataset
data = excel.ExcelDataService(fileType="attivita").getExcelData()
att = st.selectbox(label = "Seleziona una attività", options=["Preparazione Terreno ⛏️", "Irrigazione 💦", "Rincalzatura 🚜"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

if att == "Preparazione Terreno ⛏️":
    data_filtered = data_filtered[["id_activity", "Data","Attività", "Settore Orto", "mq","tempo impiegato",
                                   "Zappare", "Concimare", "Paciamatura","Protezione e reti", "Taglio Erba", "Tempo atmosferico", "Note"]]
elif att == "Rincalzatura 🚜":
    data_filtered = data_filtered[["id_activity","Data","Attività", "Settore Orto", "tempo impiegato", "Tempo atmosferico","Note"]]
else:
    data_filtered = data_filtered[["id_activity", "Data","Attività","Tempo atmosferico","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}")

if st.button("❌ Elimina Attività selezionata"):
    row_id_att = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService(fileType="attivita").deleteExcelRow(row_id_att)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")

# Add divider
st.divider()

# Purchases data
st.subheader("Consulta i tuoi dati di Acquisto 💰")

# Add dataset
data = excel.ExcelDataService(fileType="acquisti").getExcelData()
att = st.selectbox(label = "Seleziona una attività", options=["Preparazione Terreno ⛏️", "Irrigazione 💦",
                                                              "Rincalzatura 🚜", "Trattamenti 🧪","Seminare 🫘","Piantare 🌱", "Raccogliere 🍎"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

data_filtered = data_filtered[["id_activity","Data","Attività","Settore Orto","Prezzo","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}")

if st.button("❌ Elimina Acquisto selezionato"):
    row_id_att = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService(fileType="acquisti").deleteExcelRow(row_id_att)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")