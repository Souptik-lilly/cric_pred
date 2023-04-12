# Dynamic UI for IPL Prediction using Python Streamlit

## Procedure to Run the application
1. Run the python file refresh.py
    - This will keep the streamlit application updated every 20 seconds
    - python -m refresh.py
2. Run the python file data_creation.py
    - This will create live IPL data for testing
    - python -m data_creation.py
3. Run the python file app.py
    - This will generate the UI
    - python -m streamlit run app.py

## Requirements
1. Python 3.x
2. Python packages
    - matplotlib==3.7.1
    - plotly==5.13.1
    - streamlit==1.20.0
    - pandas==1.5.3
    - numpy==1.24.2