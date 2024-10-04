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
new_columns['hr'] = 'hour'
hour_df.rename(columns=new_columns, inplace=True)
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

SEASONS = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
WEATHERS = {1: 'Clear', 2: 'Cloudy/Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
day_df['season'] = day_df['season'].map(SEASONS)
day_df['weather'] = day_df['weather'].map(WEATHERS)

# Sidebar for navigation
st.sidebar.title("Navigation 📊")
section = st.sidebar.selectbox("Go to:", ['Cuaca dan Musim', 'Hari Kerja & Hari Libur', 'Kecepatan Angin & Kelembapan', 'Tren Penyewaan', 'RFM Analysis'])

# Columns layout for a cleaner look
st.markdown("<hr>", unsafe_allow_html=True)
cols = st.columns([1, 3])
# with cols[0]:
#     st.write("## Key Insights")
#     st.metric("Total Rentals", day_df['count'].sum())
#     st.metric("Average Rentals", day_df['count'].mean())

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

if section == 'Cuaca dan Musim':
    st.header("Bagaimana Cuaca dan Musim Memengaruhi Jumlah Sepeda yang Disewa?")
    st.write("Pada bagian ini, kita akan mengeksplorasi bagaimana berbagai kondisi cuaca dan musim memengaruhi penyewaan sepeda.")

    season_day_df = day_df.groupby('season').agg({'count': 'sum'}).reset_index()
    weather_day_df = day_df.groupby('weather').agg({'count': 'sum'}).reset_index()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Jumlah Penyewaan Berdasarkan Musim")
        st.write(season_day_df)
    
    with col2:
        st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
        st.write(weather_day_df)

    st.subheader("Penyewaan Sepeda Berdasarkan Cuaca dan Waktu")
    weather_hour_df = hour_df.groupby('weather').agg({
        'count': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    weather_hour_df['weather'] = weather_hour_df['weather'].map(WEATHERS)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="weather", y="count", data=weather_day_df, palette=colors, ax=ax[0])
    ax[0].set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca', fontsize=15)
    ax[0].set_xlabel('Cuaca', fontsize=12)
    ax[0].set_ylabel('Jumlah Penyewaan', fontsize=12)
    ax[0].set_yscale('log')

    sns.barplot(x="season", y="count", data=season_day_df.sort_values(by='count', ascending=False), palette=colors, ax=ax[1])
    ax[1].set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=15)
    ax[1].set_xlabel('Musim', fontsize=12)
    ax[1].set_ylabel('Jumlah Penyewaan', fontsize=12)

    st.pyplot(fig)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weather", y="count", data=weather_hour_df, palette="Purples", ax=ax1)
    ax1.set_yscale('log')
    ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca per Jam', fontsize=15)
    ax1.set_xlabel('Cuaca', fontsize=12)
    ax1.set_ylabel('Jumlah Penyewaan (log)', fontsize=12)
    
    st.pyplot(fig1)

    season_weather_day_df = day_df.groupby(['season', 'weather']).agg({
        'count': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='count', hue='weather', data=season_weather_day_df, ax=ax2, palette='pastel')

    ax2.set_title('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Musim dan Cuaca', fontsize=15)
    ax2.set_xlabel('Musim', fontsize=12)
    ax2.set_ylabel('Jumlah Penyewaan', fontsize=12)
    ax2.set_yscale('log')

    st.pyplot(fig2)

    st.caption('Cuaca sangat mempengaruhi jumlah sepeda yang disewa. Jumlah sepeda yang disewa saat cuaca clear sangat berbeda jauh dengan cuaca lainnya. Sementara itu, saat cuaca heavy rain/snow, hampir tidak ada sepeda yang disewa. Selain cuaca, musim juga mempengaruhi jumlah sepeda yang disewa. Jumlah sepeda yang disewa mencapai puncak saat musim fall dan paling sedikit saat musim spring.')

if section == 'Hari Kerja & Hari Libur':
    st.header("Apa pengaruh hari kerja dan hari libur terhadap jumlah penyewaan sepeda?")
    
    libur_count = len(day_df[day_df['workingday'] == 0])
    kerja_count = len(day_df[day_df['workingday'] == 1])

    work_or_holiday_day_df = day_df.groupby('workingday').agg({
        'count': 'sum',
    }).reset_index()
    work_or_holiday_day_df['day_count'] = [libur_count, kerja_count]
    work_or_holiday_day_df['average'] = work_or_holiday_day_df['count'] // work_or_holiday_day_df['day_count']

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=['Hari Libur', 'Hari Kerja'], y=work_or_holiday_day_df['average'], palette='pastel')
    ax.set_title('Rata-rata Penyewaan Berdasarkan Hari Kerja dan Hari Libur')
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    
    st.pyplot(fig)

    st.caption('Hari kerja dan hari libur tidak mempengaruhi penyewaan sepeda. Hal ini berdasarkan jumlah rata-rata penyewaan sepeda per hari saat hari libur dan hari kerja hampir sama, yaitu 4330 saat hari libur dan 4584 saat hari kerja.')
    
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
    ax1.set_ylabel('')


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
    ax2.set_ylabel('')

    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)

    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig2)

    st.caption('Kecepatan angin agak berpengaruh terhadap penyewaan sepeda. Hal ini berdasarkan grafik yang telah dipaparkan, ketika kecepatan angin tinggi, jumlah penyewa sepeda cenderung turun. Sementara itu, kelembapan tidak terlalu mempengaruhi penyewaan sepeda.')

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

    st.caption('Tren penyewaan meningkat dari tahun ke tahunnya, bahkan hampir mencapai dua kali lipatnya.')
if section == 'RFM Analysis':
    ## Analisis Lanjutan

    #### Rfm Analysis

    """#####  Recency """

    recent_day = day_df[day_df['date'] == day_df['date'].max()][['casual', 'registered']]
    recent_24hour = hour_df[hour_df['date'] == hour_df['date'].max()][['hour', 'casual', 'registered']]
    recent_hour = recent_24hour[recent_24hour['hour'] == recent_24hour['hour'].max()][['casual', 'registered']]

    recent_24hour = recent_24hour.melt(id_vars='hour', var_name='type', value_name='count')

    recent_24hour.head()

    customer_type = ['casual', 'registered']

    fig, ax = plt.subplots(ncols=3, figsize=(24, 6))
    sns.barplot(x=customer_type, y=recent_day.iloc[0], palette='pastel', ax=ax[0])
    ax[0].set_title('Most recent day')
    ax[0].tick_params(axis ='y', labelsize=12)
    ax[0].set_ylabel('')

    sns.barplot(x=customer_type, y=recent_hour.iloc[0], palette='pastel', ax=ax[1])
    ax[1].set_title('Most recent hour')
    ax[1].tick_params(axis ='y', labelsize=12)
    ax[1].set_ylabel('')

    sns.lineplot(x='hour', y='count', hue='type', data=recent_24hour, palette='pastel', ax=ax[2])
    ax[2].set_title('Most recent 24 hour')
    ax[2].tick_params(axis ='y', labelsize=12)
    ax[2].set_ylabel('')

    st.pyplot(fig)

    st.caption('Customer dalam 1 jam dan 1 hari terakhir didominasi oleh registered customer.')

    """##### Frequency"""

    year_df = day_df.groupby(by='year').agg({
        'count': 'sum',
        'casual':'sum',
        'registered': 'sum'
    }).reset_index()


    type_customer = ['casual', 'registered']

    year_melted_df = pd.melt(year_df, id_vars=['year'], value_vars=type_customer,
                        var_name='customer_type', value_name='count_sum')
    year_melted_df['year'] = year_melted_df['year'].map({
        0: '2011',
        1: '2012',
    })

    fig1, ax1 = plt.subplots(ncols=2, figsize=(24, 8))

    sns.barplot(x='year', y='count_sum', data=year_melted_df, hue='customer_type', palette='pastel', ax=ax1[0])
    ax1[0].set_title('Jumlah penyewaan sepeda per tahun berdasarkan tipe customer', fontsize=14)
    ax1[0].tick_params(axis ='y', labelsize=12)

    total_per_type = year_melted_df.groupby('customer_type')['count_sum'].sum()
    total_per_type = total_per_type.reset_index()
    sns.barplot(x=customer_type, y='count_sum', data=total_per_type, palette='pastel', ax=ax1[1])
    ax1[1].set_title('Jumlah total penyewaan sepeda berdasarkan tipe customer', fontsize=14)
    ax1[1].tick_params(axis ='y', labelsize=12)

    st.pyplot(fig1)
    st.caption('Jumlah frekuensi penyewaan sepeda didominasi oleh registered customer.')

    """##### Monetary"""    

    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    monthly_df = day_df[['date', 'count']].resample(rule='ME', on='date').sum().reset_index()

    max_2011 = monthly_df[:12]['count'].max()
    min_2011 = monthly_df[:12]['count'].min()

    max_2012 = monthly_df[12:]['count'].max()
    min_2012 = monthly_df[12:]['count'].min()

    fig2, ax2 = plt.subplots(1, 2, figsize=(14, 6))

    palette = sns.color_palette("coolwarm", 12)

    sns.histplot(data=monthly_df[:12], x=MONTHS, weights='count', discrete=True, ax=ax2[0], kde=True,
                palette=palette)
    ax2[0].set_title('Jumlah Pengguna per Bulan Tahun 2011')
    ax2[0].tick_params(axis='x', rotation=45)
    ax2[0].set_ylim(0, 2.5e5)

    ax2[0].bar(MONTHS[monthly_df[:12]['count'].idxmax()], max_2011, color='red', label='Max Value')
    ax2[0].bar(MONTHS[monthly_df[:12]['count'].idxmin()], min_2011, color='blue', label='Min Value')

    sns.histplot(data=monthly_df[12:], x=MONTHS, weights='count', discrete=True, ax=ax2[1], kde=True,
                palette=palette)
    ax2[1].set_title('Jumlah Pengguna per Bulan Tahun 2012')
    ax2[1].tick_params(axis='x', rotation=45)
    ax2[1].set_ylim(0, 2.5e5)

    ax2[1].bar(MONTHS[monthly_df[12:]['count'].idxmax() - 12], max_2012, color='red', label='Max Value')
    ax2[1].bar(MONTHS[monthly_df[12:]['count'].idxmin() - 12], min_2012, color='blue', label='Min Value')

    ax2[0].legend()
    ax2[1].legend()

    st.pyplot(fig2)
    st.caption('Jumlah frekuensi penyewaan sepeda didominasi oleh registered customer.')


    pengguna_2011 = year_df['count'][0]
    pengguna_2012 = year_df['count'][1]

    st.markdown(f"Jumlah pengguna sepeda tahun `2011`: `{pengguna_2011}`")
    st.markdown(f"Jumlah pengguna sepeda tahun `2012`: `{pengguna_2012}`")
    st.markdown(f"Jumlah pengguna sepeda `total`: `{pengguna_2011 + pengguna_2012}`")


# Footnotes
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("#### Dashboard created with 💡 by github.com/lutfihidayanto", unsafe_allow_html=True)
