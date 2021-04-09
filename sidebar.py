import datetime
import streamlit as st

class SideBar():
    def __init__(self):
        pass

    model = st.sidebar.selectbox(
        'Model',
        ('Seasonal-Trend decomposition', 'ARIMA',)
    )
    ihd = st.sidebar.date_input('In Home', value=datetime.datetime.now().date()) 
    fx_period = st.sidebar.slider('Forecast Period', min_value=1, max_value=90, value=90, step=None)
