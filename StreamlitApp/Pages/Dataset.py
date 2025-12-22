import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner import get_script_run_ctx

st.set_page_config(layout="wide")

st.title("Il tuo Dataset 🧮")
st.subheader("Consulta i tuoi dati")

# Add dataset
data = excel.ExcelDataService().getExcelData()[["id_activity", "Data","Attività","Prodotto","Quantità","Peso","Tempo atmosferico","Note"]]
st.dataframe(data, width='stretch')

# Colonna per selezione
selected_idx = st.selectbox("Seleziona riga da eliminare", data.index, format_func=lambda x: f"attività {x} - {data.loc[x,'Data']} - {data.loc[x,'Attività']} - {data.loc[x,'Prodotto']}")

if st.button("❌ Elimina riga selezionata"):
    row_id = data.loc[selected_idx, "id_activity"]
    try:
        excel.ExcelDataService().deleteExcelRow(row_id)
        st.session_state.data = data.drop(selected_idx).reset_index(drop=True)
        st.rerun()
        #st.success(f"attività {selected_idx} eliminata ✅")
    except Exception as e:
        st.error(f"Errore: {e}")