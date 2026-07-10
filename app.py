import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Dashboard Monitoring Tera",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Monitoring Tera")

# ==================================================
# MEMBACA DATA
# ==================================================
@st.cache_data(ttl=2)
def load_data():
    return pd.read_excel("data/datatera.xlsx")

df = load_data()

# ==================================================
# URUTAN BULAN
# ==================================================
urutan_bulan = [
    "Januari","Februari","Maret","April",
    "Mei","Juni","Juli","Agustus",
    "September","Oktober","November","Desember"
]

df["Bulan"] = pd.Categorical(
    df["Bulan"],
    categories=urutan_bulan,
    ordered=True
)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.header("Filter")

tahun = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua"] + sorted(df["Tahun"].unique().tolist())
)

bulan = st.sidebar.selectbox(
    "Pilih Bulan",
    ["Semua"] + urutan_bulan
)

# ==================================================
# FILTER DATA
# ==================================================
df_filter = df.copy()

if tahun != "Semua":
    df_filter = df_filter[df_filter["Tahun"] == tahun]

if bulan != "Semua":
    df_filter = df_filter[df_filter["Bulan"] == bulan]

# ==================================================
# DATA GRAFIK
# ==================================================
grafik = (
    df_filter
    .groupby(["Bulan", "Jenis UTTP"], observed=True)["Jumlah"]
    .sum()
    .reset_index()
)

grafik["Bulan"] = pd.Categorical(
    grafik["Bulan"],
    categories=urutan_bulan,
    ordered=True
)

grafik = grafik.sort_values("Bulan")

# ==================================================
# MEMBUAT GRAFIK
# ==================================================
fig = px.bar(
    grafik,
    x="Bulan",
    y="Jumlah",
    color="Jenis UTTP",
    text="Jumlah",
    barmode="stack",
    title="Jumlah Tera per Bulan Berdasarkan Jenis UTTP"
)

# Angka berada di dalam batang
fig.update_traces(
    textposition="inside"
)

# ==================================================
# MENAMPILKAN TOTAL DI ATAS BATANG
# ==================================================
total = (
    df_filter
    .groupby("Bulan", observed=True)["Jumlah"]
    .sum()
    .reset_index()
)

total["Bulan"] = pd.Categorical(
    total["Bulan"],
    categories=urutan_bulan,
    ordered=True
)

total = total.sort_values("Bulan")

for i in range(len(total)):
    fig.add_annotation(
        x=total.iloc[i]["Bulan"],
        y=total.iloc[i]["Jumlah"],
        text=f"Total : {int(total.iloc[i]['Jumlah'])}",
        showarrow=False,
        yshift=18,
        font=dict(size=12, color="black")
    )

# ==================================================
# TAMPILAN GRAFIK
# ==================================================
fig.update_layout(
    template="plotly_white",
    xaxis_title="Bulan",
    yaxis_title="Jumlah Tera",
    legend_title="Jenis UTTP",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TABEL
# ==================================================
st.subheader("📄 Data Monitoring")

st.dataframe(
    df_filter,
    use_container_width=True,
    hide_index=True
)