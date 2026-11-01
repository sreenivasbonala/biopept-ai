#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Launching BioPept-AI..."
streamlit run app.py
