import streamlit as st
from model_utils import load_data, get_trained_model, FITUR

df = load_data()
scaler, km, info_segmen = get_trained_model()
df["Segmen"] = [info_segmen[c]["nama"] for c in km.labels_]

st.title("Segmentasi Profil & Perilaku Nasabah Kartu Kredit")
st.markdown(
    "Pemetaan **660 nasabah** berdasarkan kapasitas limit kredit, jumlah kepemilikan kartu, "
    "serta preferensi kanal layanan (kantor cabang, perbankan online, dan panggilan CS)."
)

# Baris KPI Ringkas
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Populasi Nasabah", f"{len(df):,}")
k2.metric("Rata-Rata Limit Kredit", f"${df['Avg_Credit_Limit'].mean():,.0f}")
k3.metric("Algoritma Optimal", "K-Means (k = 3)")
k4.metric("Kualitas Klaster (Silhouette)", "0.5157")

st.divider()
st.subheader("Tiga Persona Utama Nasabah")

ringkasan_segmen = df.groupby("Segmen").agg(
    Jumlah=("Customer Key", "count"),
    Limit_Rata2=("Avg_Credit_Limit", "mean"),
    Kartu_Rata2=("Total_Credit_Cards", "mean"),
    Bank_Rata2=("Total_visits_bank", "mean"),
    Online_Rata2=("Total_visits_online", "mean"),
    CS_Rata2=("Total_calls_made", "mean"),
).reset_index()

cols = st.columns(3)
ikon_persona = ["📞", "🏦", "🌐"]

cols = st.columns(3)

for idx, row in ringkasan_segmen.iterrows():
    porsi = (row["Jumlah"] / len(df)) * 100
    segmen = row["Segmen"]

    if "Prioritas" in segmen:
        ikon = "🌐"
        kanal_dominan = f"Online ({row['Online_Rata2']:.1f}x)"
    elif "Menengah" in segmen:
        ikon = "🏦"
        kanal_dominan = f"Cabang Bank ({row['Bank_Rata2']:.1f}x)"
    else:
        ikon = "📞"
        kanal_dominan = f"Telepon CS ({row['CS_Rata2']:.1f}x)"

    with cols[idx]:
        with st.container(border=True):
            st.markdown(f"#### {ikon} {segmen}")
            st.metric("Proporsi Nasabah", f"{row['Jumlah']} orang ({porsi:.1f}%)")
            st.markdown(
                f"- **Rata-rata Limit:** ${row['Limit_Rata2']:,.0f}\n"
                f"- **Rata-rata Kartu:** {row['Kartu_Rata2']:.1f} kartu\n"
                f"- **Kanal Dominan:** {kanal_dominan}"
            )