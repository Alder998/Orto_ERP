import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel

st.set_page_config(layout="wide")

st.title("Il tuo Dataset 🧮")
st.subheader("Consulta i tuoi dati")

# Add dataset
data = excel.ExcelDataService().getExcelData()
att = st.selectbox(label = "Seleziona una attività", options=["Zappare ⛏️", "Concimare 💩", "Paciamatura 👻", "Irrigazione 💦",
                                                "Trattamenti 🧪", "Protezioni e reti 🔰", "Taglio erba 🚜", "Raccogliere 🍎",
                                                "Seminare 🫘","Piantare 🌱"])
attivita_no_emoji = att.replace(" ⛏️", "").replace(" 💩", "").replace(" 👻", "").replace(" 💦", "").replace(" 🧪", "").replace(" 🔰", "").replace(" 🚜", "").replace(" 🍎", "").replace(" 🫘", "").replace(" 🌱", "")
data_filtered = data[data["Attività"] == attivita_no_emoji]

if (att == "Raccogliere 🍎") | (att == "Seminare 🫘") | (att == "Piantare 🌱"):
    data_filtered = data_filtered[["id_activity", "Data","Attività","Prodotto","Quantità","Peso","Prezzo","Tempo atmosferico","Note"]]
elif (att == "Concimare 💩"):
    data_filtered = data_filtered[["id_activity","Data","Attività","Prodotto chimico","Prezzo","Tempo atmosferico","Note"]]
elif (att == "Trattamenti 🧪"):
    data_filtered = data_filtered[["id_activity","Data","Attività","Prodotto","Prodotto chimico","Prezzo","Tempo atmosferico","Note"]]
elif (att == "Irrigazione 💦"):
    data_filtered = data_filtered[["id_activity","Data","Attività", "Acqua utilizzata", "Tempo atmosferico","Note"]]
else:
    data_filtered = data_filtered[["id_activity","Data","Attività","Tempo atmosferico","Note"]]

st.dataframe(data_filtered, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data_filtered.index, format_func=lambda x: f"attività {x} - {data_filtered.loc[x,'Data']} - {data_filtered.loc[x,'Attività']}")

if st.button("❌ Elimina riga selezionata"):
    row_id = data_filtered.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService().deleteExcelRow(row_id)
        st.session_state.data_filtered = data_filtered.drop(selected_idx).reset_index(drop=True)
        st.rerun()
    except Exception as e:
        st.error(f"Errore: {e}")