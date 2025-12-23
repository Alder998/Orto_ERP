@echo off
title Avvio App Streamlit

echo ================================
echo Aggiornamento applicazione...
echo ================================

git pull

echo.
echo ================================
echo Installazione dipendenze...
echo ================================

python -m pip install -r requirements.txt

echo.
echo ================================
echo Avvio applicazione...
echo ================================

streamlit run App_launcher.py
