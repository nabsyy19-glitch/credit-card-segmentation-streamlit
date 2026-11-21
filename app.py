import streamlit as st

st.set_page_config(
    page_title="Credit Card Customer Segmentation",
    page_icon="💳",
    layout="wide",
)

# Sidebar berfungsi sebagai panel kontrol & info proyek
with st.sidebar:
    st.markdown("### 💳 CreditSense Analytics")
    st.caption("Sistem Segmentasi Nasabah Kartu Kredit Berbasis Unsupervised Learning")
    st.divider()

    st.markdown("**Konfigurasi Eksperimen**")
    k_selected = st.select_slider(
        "Jumlah Segmen (k) pada Lab Model:",
        options=[2, 3, 4, 5, 6],
        value=3,
    )
    st.session_state["k_selected"] = k_selected

    st.divider()
    st.markdown("**Penyusun Proyek**")
    st.caption(
        "Abednego Michael Kapelle - 241011402702\n\n"
        "Anggrillya Salwa Irawan - 241011401975\n\n"
        "Muhammad Daffa Nabil Ayyasy - 241011400637\n\n"
        "Kelas 05TPLP016 • Teknik Informatika\n"
        "Universitas Pamulang"
    )
# Navigasi di bagian atas (berbeda dari contoh yang memakai sidebar)
pages = [
    st.Page("views/ringkasan.py", title="Ringkasan & Persona", icon="🎯", default=True),
    st.Page("views/lab_model.py", title="Lab Eksplorasi & Model", icon="🔬"),
    st.Page("views/simulasi.py", title="Simulasi & Prediksi Massal", icon="⚡"),
    st.Page("views/strategi.py", title="Rekomendasi Bisnis", icon="🧭"),
]

pg = st.navigation(pages, position="top")
pg.run()