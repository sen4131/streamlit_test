import datetime
import streamlit as st
import pandas as pd
from pandasql import sqldf
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
import altair as alt
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

sns.set_style('darkgrid')
pysqldf = lambda q: sqldf(q, globals())
df = pd.read_excel('./data.xlsx', parse_dates=False)

########
#Sidebar
########
model = st.sidebar.selectbox(
    'Model',
    ('Seasonal-Trend decomposition', 'ARIMA',)
)
ihd = st.sidebar.date_input('In Home', value=datetime.datetime.now().date()) 
fx_period = st.sidebar.slider('Forecast Period', min_value=1, max_value=90, value=90, step=None)


##################
# ALL QUERIES USED
##################
q = '''
SELECT substr(`In Home`,1,10) IHD
    ,Day
    ,`Gross Calls` 
FROM df;
'''

q2 = '''
SELECT substr(`In Home`,1,10) IHD
, SUM(`Gross Calls`)
FROM df
GROUP BY substr(`In Home`,1,10);
'''

q3 = f'''
SELECT Day
, ROUND(AVG(`Gross Calls`),0) as Gross_Calls
FROM df
WHERE Day between 1 and {fx_period}
GROUP BY Day
ORDER BY 1;
'''

####################
#Pre-processing data
####################

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
c = alt.Chart(df_adj).mark_line().encode(
    x='Day',
    y='Gross Calls',
    color='IHD'
)
st.altair_chart(c, use_container_width=True)

# st.table(df_fx)
range = pd.date_range(start=ihd, periods=len(df_fx['Gross_Calls']), freq='D')
df_fx1 = df_fx.set_index(range)['Gross_Calls']
# st.write(df_fx1)


st.subheader("Time-series Modeling")
if model == 'Seasonal-Trend decomposition':
    stl = STL(df_fx1, seasonal=7,  robust=True)
    res = stl.fit()
    fig = res.plot()
    st.pyplot(fig)
