# import datetime
import streamlit as st
import pandas as pd
from pandasql import sqldf
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
import altair as alt
# import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
#local
from queries import *
from css import *
from sidebar import SideBar

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# sns.set_style('darkgrid')
pysqldf = lambda q: sqldf(q, globals())
df = pd.read_excel('./data.xlsx', parse_dates=False)

########
#Sidebar
########

SideBar()
fx_period = SideBar().fx_period
ihd = SideBar().ihd
model = SideBar().model

####################
#Pre-processing data
####################

q3 = q3(fx_period)

# Summary data on each IHD
df_agg = pysqldf(q2)

#df adjusted for chart
df_adj = pysqldf(q)

#aggregated campaign for forecasting
df_fx = pysqldf(q3)


#####
#Body
#####

st.title('Stats data')

st.subheader("Sample data")
st.table(df_agg.set_index('IHD'))

st.subheader("Time-series Plot")
c = alt.Chart(df_adj)\
    .mark_line()\
    .encode(
    x='Day',
    y='Gross Calls',
    color='IHD',
) 

st.altair_chart(c, use_container_width=True)

range = pd.date_range(start=ihd, periods=len(df_fx['Gross_Calls']), freq='D')
df_fx1 = df_fx.set_index(range)['Gross_Calls']

st.subheader("Time-series Modeling")
if model == 'Seasonal-Trend decomposition':
    stl = STL(df_fx1, seasonal=7,  robust=True)
    res = stl.fit()
    fig = res.plot()
    st.pyplot(fig)


