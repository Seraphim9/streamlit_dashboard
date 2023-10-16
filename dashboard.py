#Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Menyiapkan rental_df 
def create_rental_df(df):
    rental_df = df.groupby(df['datetime'].dt.date).agg({
        'count':'sum'
    }).reset_index()
    return rental_df

#Baca dataset
rental_df = pd.read_csv("day_rental_df.csv")

datetime_columns = ["datetime"]
rental_df['datetime'] = pd.to_datetime(rental_df['datetime'])

#Membuat filter
min_date = rental_df["datetime"].min()
max_date = rental_df["datetime"].max()
 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = rental_df[(rental_df["datetime"] >= str(start_date)) & 
                (rental_df["datetime"] <= str(end_date))]

#Membuat judul dan subheader
st.header('Dashboard Sederhana Bike Sharing')
st.subheader('Oleh Muhammad Zhillan Zaini')
st.caption('Dashboard dibuat berdasarkan tugas latihan')

#Visualisasi Total penyewaan
st.subheader('Total Penyewaan Sepeda')
total_orders = rental_df['count'].sum()
st.metric("Total Penyewaan", value=total_orders)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df['datetime'],
    main_df['count'],
    marker='o',
    linewidth =2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

#Tabs untuk masing-masing visualisasi berdasarkan musim, cuaca, dan jenis hari
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.subheader("Pengaruh Musim")
    season_counts = rental_df[['season', 'count']]

    season_counts['season'] = season_counts['season'].map({
        1: 'Spring', 
        2: 'Summer', 
        3: 'Fall', 
        4: 'Winter'
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]
    sns.barplot(x='season', y='count', data=season_counts, errorbar=None, palette=colors, ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_title('Tren Pengaruh Musim Terhadap Penyewaan Sepeda')

    st.pyplot(fig)

with tab2:
    st.subheader("Pengaruh Cuaca")
    weather_count = rental_df[['weather', 'count']]

    weather_count['weather'] = weather_count['weather'].map({
        1: 'Clear; Few clouds',
        2: 'Mist; Cloudy',
        3: 'Light Snow; Light Rain',
        4: 'Heavy Rain; Thunderstorm'
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#D3D3D3", "#72BCD4", "#D3D3D3"]
    sns.barplot(x='weather', y='count', data=weather_count, errorbar=None, palette=colors, ax=ax)
    ax.set_xlabel('Cuaca')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_title('Tren Pengaruh Cuaca Terhadap Penyewaan Sepeda')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    st.pyplot(fig)

with tab3:
    st.subheader("Berdasarkan Jenis Hari")
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",
          "#D3D3D3", "#72BCD4", "#D3D3D3"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=rental_df, x='weekday', y='count', ci=None, palette=colors, ax=ax)
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_title('Pengaruh Jenis Hari terhadap Jumlah Penyewaan Sepeda')
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'], rotation=45)

    st.pyplot(fig)

st.subheader("Berdasarkan Suhu")

fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(data=rental_df, x='temp', y='count', line_kws={'color': 'red'}, ax=ax)
ax.set_xlabel('Suhu (°C)')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda')
st.pyplot(fig)

colors = {
    'Spring': 'r',  # Red
    'Summer': 'g',  # Green
    'Fall': 'b',    # Blue
    'Winter': 'y'   # Yellow
}

#menampilkan visualisasi berdasarkan suhu
st.subheader('Teknik Clustering Penyewaan Sepeda Berdasarkan Musim')

sample_size = st.slider("Jumlah Sampel", min_value=1, max_value=200, value=150)

plt.figure(figsize=(10, 6))
for cluster, color in colors.items():
    data = rental_df[rental_df['cluster'] == cluster]
    sampled_data = data.sample(n=sample_size)
    plt.scatter(sampled_data['temp'], sampled_data['count'], c=color, label=cluster, alpha=0.5)

plt.xlabel('Suhu (°C)')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Scatter Plot Penyewaan Sepeda Berdasarkan Musim')
plt.legend(title='Musim')
plt.tight_layout()

st.pyplot(plt)
