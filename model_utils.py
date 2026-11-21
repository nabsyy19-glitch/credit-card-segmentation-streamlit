import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

FITUR = [
    "Avg_Credit_Limit",
    "Total_Credit_Cards",
    "Total_visits_bank",
    "Total_visits_online",
    "Total_calls_made",
]

@st.cache_data
def load_data():
    return pd.read_csv("Credit Card Customer Data.csv")

@st.cache_resource
def get_trained_model():
    df = load_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[FITUR])

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = km.fit_predict(X_scaled)

    # Urutkan klaster berdasarkan rata-rata limit kredit agar konsisten
    df_temp = df.copy()
    df_temp["Cluster_Raw"] = clusters
    urutan = (
        df_temp.groupby("Cluster_Raw")["Avg_Credit_Limit"]
        .mean()
        .sort_values()
        .index.tolist()
    )

    info_segmen = {
        urutan[0]: {
            "nama": "Segmen Rendah (Aktif Telepon CS)",
            "rekomendasi": "Edukasi penggunaan aplikasi mobile banking & fitur FAQ mandiri untuk mengurangi panggilan CS.",
        },
        urutan[1]: {
            "nama": "Segmen Menengah (Aktif Cabang Bank)",
            "rekomendasi": "Tawarkan promo cashback transaksi rutin & migrasi layanan teller ke digital banking.",
        },
        urutan[2]: {
            "nama": "Segmen Prioritas (Aktif Layanan Online)",
            "rekomendasi": "Berikan penawaran kenaikan limit otomatis, kartu premium, & program loyalitas eksklusif.",
        },
    }
    return scaler, km, info_segmen