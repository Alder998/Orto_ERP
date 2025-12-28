import sys
import os
import streamlit as st
from pathlib import Path
import signal

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

st.markdown(
    """
    <style>
    /* Testo delle voci di navigazione (st.Page title) */
    [data-testid="stSidebarNavItems"] span {
        font-size: 18px !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

pages = [
     st.Page("Pages/Home.py", icon="🌱", default=True, title="Il tuo Orto"),
     st.Page("Pages/Diary.py", icon="🖊️", title="Diario"),
     st.Page("Pages/Purchase.py", icon="💰", title="Diario Acquisti"),
     st.Page("Pages/Dataset.py", icon="🧮", title="Dataset"),
]

nav = st.navigation(pages, position="sidebar")

# Close botton
if st.sidebar.button("❌ Chiudi applicazione"):
    st.warning("Chiusura applicazione...")
    os.kill(os.getpid(), signal.SIGTERM)

nav.run()