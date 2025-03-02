import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as mticker
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
df=pd.read_csv('Airquality_Guanyuan_Clean.csv')

def ispu_pm25(pm25):
  batas_pm25=[0,15.5,55.4,150.4,250.4,350,550,650,750]
  batas_ispu=[0,50,100,150,200,300,400,500,600]

  for i in range(len(batas_pm25)-1):
    if batas_pm25[i] <= pm25 < batas_pm25[i+1]:
      ispu_pm25=((batas_ispu[i+1]-batas_ispu[i])/ (batas_pm25[i+1]-batas_pm25[i])*(pm25 - batas_pm25[i])) +batas_ispu[i]
      return round(ispu_pm25)

def ispu_pm10(pm10):
  batas_pm10=[0,50,150,350,420,500,600,700,800,900,1000]
  batas_ispu=[0,50,100,150,200,300,400,500,600,700,800]

  for i in range(len(batas_pm10)-1):
    if batas_pm10[i] <= pm10 < batas_pm10[i+1]:
      ispu_pm10= ((batas_ispu[i+1]- batas_ispu[i])/ (batas_pm10[i+1]- batas_pm10[i])* (pm10 -batas_pm10[i])) + batas_ispu[i]
      return round(ispu_pm10)

def ispu_so2(so2):

  batas_so2=[0,52,180,400,800,1200]
  batas_ispu=[0,50,100,200,300,400]

  for i in range(len(batas_so2)-1):
    if batas_so2[i] <= so2 < batas_so2[i+1]:
      ispu_so2=((batas_ispu[i+1] - batas_ispu[i]) / (batas_so2[i+1] - batas_so2[i]) *(so2-batas_so2[i])) + batas_ispu[i]
      return round(ispu_so2)


def ispu_NO2(no2):
  batas_no2=[0,80,200,1130,2260,3000]
  batas_ispu=[0,50,100,200,300,400]

  for i in range(len(batas_no2)-1):
    if batas_no2[i] <= no2 < batas_no2[i+1]:
      ispu_no2=((batas_ispu[i+1]-batas_ispu[i])/ (batas_no2[i+1]-batas_no2[i]) * (no2-batas_no2[i])) + batas_ispu[i]
      return round(ispu_no2)

def ispu_co(co):
  batas_co=[0,4000,8000,15000,30000,40000]
  batas_ispu=[0,50,100,200,300,400]

  for i in range(len(batas_co)-1):
    if batas_co[i] <= co < batas_co[i+1]:
      ispu_co=((batas_ispu[i+1]-batas_ispu[i])/ (batas_co[i+1]-batas_co[i]) * (co-batas_co[i])) + batas_ispu[i]
      return round(ispu_co)

def ispu_o3(o3):
  batas_o3=[0,120,235,400,800,1000]
  batas_ispu=[0,50,100,200,300,400]

  for i in range(len(batas_o3)-1):
    if batas_o3[i] <= o3 < batas_o3[i+1]:
      ispu_o3=((batas_ispu[i+1]-batas_ispu[i])/ (batas_o3[i+1]-batas_o3[i]) * (o3-batas_o3[i])) + batas_ispu[i]
      return round(ispu_o3)

df['ISPU PM2.5']=df['PM2.5'].apply(ispu_pm25)
df['ISPU PM10']=df['PM10'].apply(ispu_pm10)
df['ISPU SO2']=df['SO2'].apply(ispu_so2)
df['ISPU NO2']=df['NO2'].apply(ispu_NO2)
df['ISPU CO']=df['CO'].apply(ispu_co)
df['ISPU O3']=df['O3'].apply(ispu_o3)

AV_vis= df.groupby("year")["ISPU PM2.5"].mean()
Data= AV_vis.reset_index()

def tingkatan_ispu(ISPU):
    if ISPU <=50:
        return "Baik"
    elif ISPU >50 and ISPU <=100:
        return "Sedang"
    elif ISPU >100 and ISPU <=200:
        return "Tidak Sehat"
    elif ISPU <200 and ISPU <=300:
        return "Sangat Tidak Sehat"
    elif ISPU >300:
        return "Berbahaya"

Data['Kategori']=Data["ISPU PM2.5"].apply(tingkatan_ispu)

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


st.subheader('Rata-Rata Indeks Standar Pencemaran Udara (ISPU) setiap tahun')
ISPU=plt.figure(figsize=(10,5))
plt.plot(AV_vis.index,AV_vis.values,marker='o',linestyle="-",color="b",label="Rata-Rata ISPU setiap Tahun")

plt.title("Rata-Rata ISPU per Tahun")
plt.xlabel('Tahun')
plt.title('Rata-Rata ISPU per tahun')
plt.grid(True)
plt.legend()
plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.show()
st.pyplot(ISPU)

st.subheader("Kategori ISPU setiap Tahun")

category=plt.figure(figsize=(8,5))
sns.barplot(x='year',y='ISPU PM2.5',hue='Kategori',data=Data,palette={'Sedang':'blue','Tidak Sehat':'yellow'})
plt.xlabel('Tahun')
plt.ylabel('ISPU')
plt.title('Kategori ISPU Setiap Tahun')
plt.ylim(90,110)
st.pyplot(category)