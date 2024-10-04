import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Customizing Streamlit theme
st.set_page_config(page_title="Bike Sharing Data", page_icon="🚴", layout="wide")

# Adding custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 40px;
            color: #4A90E2;
            text-align: center;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .block-container {
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Title of the Dashboard
st.markdown('<div class="main-title">Bike Sharing Data Analysis 🚴</div>', unsafe_allow_html=True)

# Load data
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Data preparation (same as before)
new_columns = {'dteday': 'date', 'yr': 'year', 'mnth': 'month', 'weathersit': 'weather', 'hum': 'humidity', 'cnt': 'count'}
day_df.rename(columns=new_columns, inplace=True)
day_df['date'] = pd.to_datetime(day_df['date'])

SEASONS = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
WEATHERS = {1: 'Clear', 2: 'Cloudy/Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
day_df['season'] = day_df['season'].map(SEASONS)
day_df['weather'] = day_df['weather'].map(WEATHERS)

# Sidebar for navigation
st.sidebar.title("Navigation 📊")
section = st.sidebar.radio("Go to:", ['Cuaca dan Musim', 'Hari Kerja & Hari Libur', 'Kecepatan Angin & Kelembapan', 'Tren Penyewaan'])

# Columns layout for a cleaner look
st.markdown("<hr>", unsafe_allow_html=True)
cols = st.columns([1, 3])
with cols[0]:
    st.write("## Key Insights")
    st.metric("Total Rentals", day_df['count'].sum())
    st.metric("Average Rentals", day_df['count'].mean())

with cols[1]:
    if section == 'Cuaca dan Musim':
        st.header("Bagaimana cuaca dan musim memengaruhi jumlah sepeda yang disewa?")
        
        season_day_df = day_df.groupby('season').agg({'count': 'sum'}).reset_index()
        weather_day_df = day_df.groupby('weather').agg({'count': 'sum'}).reset_index()

        col1, col2 = st.columns(2)
        with col1:
            st.write(season_day_df)
        with col2:
            st.write(weather_day_df)
        #hour
        weather_hour_df = hour_df.groupby('weather').agg({
            'count': 'sum',
            'casual': 'sum',
            'registered': 'sum'
        }).reset_index()
        weather_hour_df['weather'] = weather_hour_df['weather'].map(WEATHERS)
        print("hour: \n",weather_hour_df)

        season_weather_day_df = day_df.groupby(['season', 'weather']).agg({
            'count': 'sum',
            'casual': 'sum',
            'registered': 'sum'
        }).reset_index()
        season_weather_day_df['season'] = season_weather_day_df['season'].map(SEASONS)
        season_weather_day_df['weather'] = season_weather_day_df['weather'].map(WEATHERS)

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
        colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(x="weather", y="count", data=weather_day_df, palette=colors, ax=ax[0])
        ax[0].set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca', fontsize=15)
        ax[0].set_xlabel('Cuaca', fontsize=12)
        ax[0].set_ylabel('Jumlah Penyewaan', fontsize=12)

        sns.barplot(x="season", y="count", data=season_day_df.sort_values(by='count', ascending=False), palette=colors, ax=ax[1])
        ax[1].set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=15)
        ax[1].set_xlabel('Musim', fontsize=12)
        ax[1].set_ylabel('Jumlah Penyewaan', fontsize=12)

        st.pyplot(fig)

        colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

        print(f"Heavy rain: {weather_hour_df.iloc[3]['count']}")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x="weather", y="count", data=weather_hour_df, palette=colors, ax=ax1)
        ax1.set_yscale('log')
        ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca per Jam')
        ax1.set_xlabel('Cuaca')
        ax1.set_ylabel('Jumlah Penyewaan')

        st.pyplot(fig1)

        fig2, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season', y='count', hue='weather', data=season_weather_day_df, ax=ax3)

        ax3.set_title('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Musim dan Cuaca', fontsize=15)
        ax3.set_xlabel('Musim', fontsize=12)
        ax3.set_ylabel('Jumlah Penyewaan', fontsize=12)
        ax3.set_yscale('log') # gak bisa muncul

        st.pyplot(fig2)


    if section == 'Hari Kerja & Hari Libur':
        st.header("Apa pengaruh hari kerja dan hari libur terhadap jumlah penyewaan sepeda?")
        
        libur_count = len(day_df[day_df['workingday'] == 0])
        kerja_count = len(day_df[day_df['workingday'] == 1])

        work_or_holiday_day_df = day_df.groupby('workingday').agg({
            'count': 'sum',
        }).reset_index()
        work_or_holiday_day_df['day_count'] = [libur_count, kerja_count]
        work_or_holiday_day_df['average'] = work_or_holiday_day_df['count'] // work_or_holiday_day_df['day_count']

        # Plot graph
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=['Hari Libur', 'Hari Kerja'], y=work_or_holiday_day_df['average'], palette='pastel')
        ax.set_title('Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari Libur')
        ax.set_ylabel("Rata-rata Jumlah Penyewaan")
        
        st.pyplot(fig)

    if section == 'Kecepatan Angin & Kelembapan':
        st.header("Apakah ada pengaruh signifikan dari kecepatan angin atau kelembapan terhadap penyewaan sepeda?")
        
        # MinMaxScaler
        scaler = MinMaxScaler()
        windspeed_hum_normalized = scaler.fit_transform(day_df[['windspeed', 'count', 'humidity']])

        windspeed_hum_normalized_df = pd.concat([day_df['date'], pd.DataFrame(windspeed_hum_normalized, columns=['windspeed', 'count', 'humidity'])], axis=1)
        
        # Plot windspeed vs count
        fig, ax = plt.subplots(figsize=(20, 10))

        monthly_df = windspeed_hum_normalized_df.resample(on='date', rule='ME').sum().reset_index()

        sns.lineplot(x='date', y='count', data=monthly_df, label='Jumlah Penyewa', color='red', ax=ax)
        sns.lineplot(x='date', y='windspeed', data=monthly_df, label='Kecepatan Angin', color='skyblue', ax=ax)
        sns.lineplot(x='date', y='humidity', data=monthly_df, label='Kelembapan', color='grey', ax=ax)

        ax.set_title('Hubungan antara Kecepatan Angin, Kelembapan, dan Jumlah Penyewa', fontsize=16)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.legend(title='Keterangan')

        st.pyplot(fig)
            

        windspeed_day_df = day_df.groupby('windspeed').agg({
            'count': 'sum',
            'casual': 'sum',
            'registered': 'sum'
        }).reset_index()
        

        fig1, ax1 = plt.subplots(figsize=(20, 10))

        sns.histplot(data=windspeed_day_df, x='windspeed', weights='count', bins=20, color='skyblue', kde=True, stat='count',ax=ax1)

        ax1.set_title('Distribusi Jumlah Penyewa Berdasarkan Kecepatan Angin', fontsize=20, fontweight='bold')
        ax1.set_xlabel('Kecepatan Angin (km/h)', fontsize=18)
        ax1.set_ylabel('Jumlah Penyewa', fontsize=18)

        ax1.tick_params(axis='x', labelsize=14)
        ax1.tick_params(axis='y', labelsize=14)

        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig1)

        # Humidityu plot
        humidity_day_df = day_df.groupby('humidity').agg({
            'count': 'sum',
            'casual': 'sum',
            'registered': 'sum'
        }).reset_index()

        fig2, ax2 = plt.subplots(figsize=(20, 10))

        sns.histplot(data=humidity_day_df, x='humidity', weights='count', bins=20, color='skyblue', kde=True, stat='count', ax=ax2)

        ax2.set_title('Distribusi Jumlah Penyewa Berdasarkan Kelembapan', fontsize=20, fontweight='bold')
        ax2.set_xlabel('Kelembapan', fontsize=18)
        ax2.set_ylabel('Jumlah Penyewa', fontsize=18)

        ax2.tick_params(axis='x', labelsize=14)
        ax2.tick_params(axis='y', labelsize=14)

        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig2)

    if section == 'Tren Penyewaan':
        st.header("Bagaimana tren penyewaan sepeda berkembang dari tahun ke tahunnya?📈")
    
        mean_count_2011 = day_df[day_df['year'] == 0]['count'].mean()
        mean_count_2012 = day_df[day_df['year'] == 1]['count'].mean()

        st.write(f"Rata-rata penyewaan sepeda pada tahun 2011: {mean_count_2011}")
        st.write(f"Rata-rata penyewaan sepeda pada tahun 2012: {mean_count_2012}")

        # Visualize trend over time
        month_count_df = day_df.resample(on='date', rule='ME').sum().reset_index()

        # Creating figure and axis
        fig, ax = plt.subplots(figsize=(14, 6))

        # Creating a line plot
        sns.lineplot(data=month_count_df, x='date', y='count', color='red', ax=ax)

        # Setting title and labels
        ax.set_title('Jumlah Pengguna dari tahun ke tahun', fontsize=16)
        ax.set_xlabel('Tanggal', fontsize=12)
        ax.set_ylabel('Jumlah Pengguna', fontsize=12)

        # Rotating x-axis labels
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

# Footnotes
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Dashboard created with 💡 by Lutfi", unsafe_allow_html=True)
