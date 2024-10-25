import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency


airqu_df=pd.read_csv('Airquality_Guanyuan_Clean.csv')

with st.sidebar:
    col1,col2,col3=st.columns([0.3,3,0.3])
    with col2:
        st.title('Air Quality in Guanyuan City')
    col1,col2,col3=st.columns([0.5,4,0.5])
    with col2:
        st.image("https://obrablancaexpo.com/wp-content/uploads/2024/09/logo-2.jpg",width=300)
    

    year=st.selectbox(
        label="Year:",
        options=(2013,2014,2015,2016,2017)
    )


visual=airqu_df.groupby(by=["year","month"]).agg({
    "PM2.5":"mean",
    "PM10":"mean",
    "SO2":"mean",
    "NO2":"mean",
    "CO":"mean",
    "O3":"mean",
    "TEMP":"mean"
})
minmax=airqu_df.groupby(by="year").agg({
    "PM2.5":["max","min","mean"],
    "PM10":["max","min","mean"],
    "SO2":["max","min","mean"],
    "NO2":["max","min","mean"],
    "CO":["max","min","mean"],
    "O3":["max","min","mean"],
    "TEMP":["max","min","mean"]
})
minmax=minmax.round(3)
st.header('Air Quality Summary in Guanyuan City')

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('PM2.5(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["PM2.5"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["PM2.5"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["PM2.5"]["mean"].loc[year])

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('PM10(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["PM10"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["PM10"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["PM10"]["mean"].loc[year])

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('SO₂(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["SO2"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["SO2"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["SO2"]["mean"].loc[year])

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('NO₂(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["NO2"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["NO2"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["NO2"]["mean"].loc[year])

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('CO(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["CO"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["CO"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["CO"]["mean"].loc[year])


col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('O³(µg/m³)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["O3"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["O3"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["O3"]["mean"].loc[year])

col1,col2,col3=st.columns([2,3,2])
with col2:
    st.subheader('Temperature (°C)')
col1,col2,col3=st.columns([4,4,4])
with col1:
    st.metric(label="Max",value=minmax["TEMP"]["max"].loc[year])
with col2:
    st.metric(label="Min",value=minmax["TEMP"]["min"].loc[year])
with col3:
    st.metric(label="Average",value=minmax["TEMP"]["mean"].loc[year])
st.subheader('Rata-rata Polutant Pada Kota Guanyuan setiap tahun')

data=visual.loc[year]
variables=["PM2.5","PM10","SO2","NO2","CO","O3","TEMP"]
fig,axes=plt.subplots(4,2,figsize=(17,12))
axes=axes.flatten()

for i,var in enumerate(variables):
    axes[i].plot(data.index,data[var],marker="o")
    axes[i].set_title(f'Rata-rata Konsentrasi {var}')
    axes[i].set_xlabel('Month')
    axes[i].set_ylabel(f'{var} µg/m³')
    if var=="TEMP":
        axes[i].set_ylabel(f'{var} °C')

fig.delaxes(axes[-1])
plt.tight_layout(pad=2.0,w_pad=1.5,h_pad=2.0)
st.pyplot(fig)


st.subheader('Hubungan antara konsentrasi CO terhadap PM2.5 dan PM10 ')

constrated=plt.figure(figsize=(10,5))
plt.scatter(airqu_df['CO'],airqu_df['PM2.5'],marker="o",linestyle="-",color="b",label="PM2.5")
plt.scatter(airqu_df['CO'],airqu_df['PM10'],marker="o",linestyle="-",color="y",label="PM10")

plt.xlabel('Konsentrasi Polutan ((µg/m³))')
plt.ylabel('Konsentrasi CO ((µg/m³))')

plt.legend()
plt.grid()
st.pyplot(constrated)
