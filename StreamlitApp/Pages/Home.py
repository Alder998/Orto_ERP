import streamlit as st
from StreamlitApp.ExcelService import ExcelDataService as excel
import altair as alt
import copy
import pandas as pd

st.set_page_config(layout="wide")

st.title("Ciao Guido 🌱")
st.subheader("I tuoi dati e le tue attività")

st.subheader("\nLa tua ultima attività")
data = excel.ExcelDataService().getExcelData()
data["Data"] = pd.to_datetime(data["Data"], unit="ms")

# Create data_last
data_last = copy.deepcopy(data)
data_last = data_last[["Data","Attività","Tempo atmosferico","Note"]]
data_last["Data"] = data_last["Data"].dt.strftime("%d/%m/%Y")
data_last = data_last[data["Data"] == data_last["Data"].max()].reset_index(drop=True)
st.dataframe(data_last, width='stretch')

# Organize dashboard graphs for activities
st.subheader("\n\n\nLe tue attività per data")
options = list(data["Data"].dt.strftime("%Y-%m").unique())
options.insert(0, "tutte le date")
opt_att = st.selectbox(label = "Seleziona mese", options=options)
if opt_att != "tutte le date":
    data_filtered = data[pd.to_datetime(data["Data"]).dt.strftime("%Y-%m") == opt_att]
else:
    data_filtered = data
chart = (
    alt.Chart(data_filtered)
    .mark_bar()
    .encode(
        x="Data:T",
        y="count(Attività):Q",
        color="Attività:N",
        tooltip=["Attività", "Data"]
    )
)
st.altair_chart(chart)

# Organize dashboard graphs for product planted and harvested
st.subheader("\n\n\nI tuoi prodotti")
opt_prod = st.selectbox(label = "Seleziona una coltivazione", options=data["Prodotto"].dropna().unique())
data_line_chart = copy.deepcopy(data)
data_line_chart = data_line_chart[data_line_chart["Prodotto"] == opt_prod]

# Harvesting chart
data_line_chart_raccolta = data_line_chart[data_line_chart["Attività"]=="Raccogliere"]
data_line_chart_raccolta["Peso"] = data_line_chart_raccolta["Peso"].cumsum()

# Planting  and seeding chart
data_line_chart_sem_pianta = data_line_chart[data_line_chart["Attività"].isin(["Seminare","Piantare"])]
data_line_chart_sem_pianta["Prezzo"] = -data_line_chart_sem_pianta["Prezzo"]
data_line_chart_sem_pianta["Prezzo"] = data_line_chart_sem_pianta["Prezzo"].cumsum()

# Prima linea (asse sinistro)
line_right = (
    alt.Chart(data_line_chart_raccolta)
    .mark_line(point=True)
    .encode(
        x=alt.X("Data:T", title="Data"),
        y=alt.Y("Peso:Q", title="Peso (raccolto)"),
        tooltip=["Data:T", "Peso:Q"]
    )
)

# Seconda linea (asse destro)
line_left = (
    alt.Chart(data_line_chart_sem_pianta)
    .mark_line(point=True)
    .encode(
        x="Data:T",
        y=alt.Y(
            "Prezzo:Q",
            title="Prezzo € (seminato + piantato)",
            axis=alt.Axis(orient="left")
        ),
        tooltip=["Data:T", "Prezzo:Q"]
    )
)

# Layer con scale indipendenti
chart = alt.layer(line_left, line_right).resolve_scale(y="independent")

st.altair_chart(chart)