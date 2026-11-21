import streamlit as st
import pandas as pd
from model_utils import load_data, get_trained_model, FITUR

st.title("Simulasi & Batch Scoring Pelanggan")
df_ref = load_data()
scaler, km, info_segmen = get_trained_model()

tab_single, tab_batch = st.tabs(["👤 Simulasi Satu Pelanggan", "📂 Batch Scoring (Upload CSV)"])

with tab_single:
    col_form, col_hasil = st.columns([1.1, 1])
    with col_form:
        limit = st.number_input("Rata-rata Limit Kredit ($)", 1000, 500000, 45000, step=1000)
        kartu = st.slider("Jumlah Kartu Kredit", 1, 15, 5)
        bank = st.slider("Kunjungan ke Cabang Bank", 0, 15, 3)
        online = st.slider("Akses Layanan Online", 0, 20, 2)
        calls = st.slider("Panggilan Telepon ke CS", 0, 15, 2)

    with col_hasil:
        st.markdown("#### Hasil Klasifikasi Segmen Real-Time")
        inp = pd.DataFrame([[limit, kartu, bank, online, calls]], columns=FITUR)
        klaster = km.predict(scaler.transform(inp))[0]
        hasil = info_segmen[klaster]

        with st.container(border=True):
            st.success(f"**Segmen Terdeteksi:** {hasil['nama']}")
            st.write(f"**Tindakan yang Disarankan:** {hasil['rekomendasi']}")
            st.caption(
                f"Perbandingan Limit: ${limit:,} vs rata-rata seluruh nasabah (${df_ref['Avg_Credit_Limit'].mean():,.0f})."
            )

with tab_batch:
    c_info, c_dl = st.columns([2, 1])
    with c_info:
        st.write("Unggah file CSV nasabah untuk menambahkan kolom segmen dan rekomendasi strategi secara otomatis.")
    with c_dl:
        st.download_button(
            "⬇️ Unduh Contoh Format CSV",
            data=df_ref.head(15).to_csv(index=False).encode("utf-8"),
            file_name="contoh_data_nasabah.csv",
            mime="text/csv",
        )

    file_csv = st.file_uploader("Pilih file CSV", type=["csv"])
    if file_csv is not None:
        df_up = pd.read_csv(file_csv)
        kurang = [c for c in FITUR if c not in df_up.columns]
        if kurang:
            st.error(f"Kolom wajib tidak ditemukan: {', '.join(kurang)}")
        else:
            pred = km.predict(scaler.transform(df_up[FITUR]))
            df_up["Segmen_Pelanggan"] = [info_segmen[p]["nama"] for p in pred]
            df_up["Rekomendasi_Strategi"] = [info_segmen[p]["rekomendasi"] for p in pred]

            pilihan = st.multiselect(
                "Filter Segmen yang Ditampilkan:",
                options=df_up["Segmen_Pelanggan"].unique().tolist(),
                default=df_up["Segmen_Pelanggan"].unique().tolist(),
            )
            df_filtered = df_up[df_up["Segmen_Pelanggan"].isin(pilihan)]
            st.dataframe(df_filtered, use_container_width=True)

            st.download_button(
                f"💾 Simpan Hasil Segmentasi ({len(df_filtered)} baris)",
                data=df_filtered.to_csv(index=False).encode("utf-8"),
                file_name="hasil_segmentasi_kartu_kredit.csv",
                mime="text/csv",
            )