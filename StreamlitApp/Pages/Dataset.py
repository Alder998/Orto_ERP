import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel
import pandas as pd

st.set_page_config(layout="wide")

st.title("Il tuo Dataset 🧮")
st.subheader("Consulta i tuoi dati di produzione 🍎")

# Add dataset
data = excel.ExcelDataService(fileType="produzione").getExcelData()
data["Data"] = pd.to_datetime(data["Data"]).dt.strftime("%d/%m/%Y")
att = st.selectbox(label = "Seleziona una attività", options=["Trattamenti 🧪","Seminare 🫘","Piantare 🌱", "Germinazione 🌼", "Raccogliere 🍎"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "").replace(" 🌼", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

if (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    data_filtered = data_filtered[["id_activity", "Data","Attività", "Settore Orto", "Prodotto","Quantità","Tempo atmosferico","Note"]]
elif (att == "Raccogliere 🍎"):
    data_filtered = data_filtered[["id_activity", "Data","Attività", "Settore Orto","Prodotto","Peso","Prezzo stimato","Tempo atmosferico","Note"]]
elif (att == "Trattamenti 🧪"):
    data_filtered = data_filtered[["id_activity","Data","Attività", "Settore Orto","Prodotto","Prodotto chimico","Tempo atmosferico","Note"]]
else:
    data_filtered = data_filtered[["id_activity","Data","Attività", "Settore Orto","Tempo atmosferico","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}", key="Prod_Delete")

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
data["Data"] = pd.to_datetime(data["Data"]).dt.strftime("%d/%m/%Y")
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
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}", key="Att_Delete")

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
data["Data"] = pd.to_datetime(data["Data"]).dt.strftime("%d/%m/%Y")
att = st.selectbox(label = "Seleziona una attività", options=["Forniture 💦", "Carburante 🛢️", "Attrezzatura ⛏️",
                                                              "Concimi/terriccio 💩", "Trattamenti 🧪", "Sementi 🫘", "Piantine 🌱"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "").replace(" 🛢️", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

data_filtered = data_filtered[["id_activity","Data","Fornitore","Attività","Prezzo","Note","Prodotto","Quantità"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']} - {data_filtered.loc[x,'Note']}", key="Acq_Delete")

if st.button("❌ Elimina Acquisto selezionato"):
    row_id_att = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService(fileType="acquisti").deleteExcelRow(row_id_att)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")

# Add the dataset on the Terrario part
# Add divider
st.divider()

# Purchases data
st.subheader("Consulta qui i tuoi dati sul terrario 🐸")

# Add dataset
data_greenhouse = excel.ExcelDataService(fileType="terrario").getExcelData()
data_greenhouse["Data"] = pd.to_datetime(data_greenhouse["Data"]).dt.strftime("%d/%m/%Y")
att = st.selectbox(label = "Seleziona una attività", options=["Seminare 🫘", "Raccogliere 🍎"])

attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "").replace(" 🛢️", "")
data_filtered = data_greenhouse[data_greenhouse["Attività"] == attivita_no_emoji]

data_filtered = data_filtered[["id_activity","Data","Attività","Prodotto","tempo impiegato","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona attività terrario da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']} - {data_filtered.loc[x,'Note']}", key="greenhouse_Delete")

if st.button("❌ Elimina Attività Terrario selezionata"):
    row_id_att = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService(fileType="acquisti").deleteExcelRow(row_id_att)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")