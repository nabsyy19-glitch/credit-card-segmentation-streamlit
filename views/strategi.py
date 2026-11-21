import streamlit as st

st.title("Strategi Bisnis & Evaluasi Akhir")

st.markdown("""
Hasil pemodelan K-Means ($k=3$) memberikan dasar pengambilan keputusan yang terukur bagi divisi pemasaran dan operasional kartu kredit:
""")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("### 🌐 Segmen Prioritas")
        st.caption("Limit tinggi (~$141.000) & sangat aktif di kanal digital.")
        st.markdown(
            "- Tawarkan kartu *co-branding* premium & fasilitas *airport lounge*.\n"
            "- Otomatisasi kenaikan limit kredit berkala.\n"
            "- Kirimkan penawaran eksklusif langsung via notifikasi aplikasi."
        )

with col2:
    with st.container(border=True):
        st.markdown("### 🏦 Segmen Menengah")
        st.caption("Limit moderat (~$33.700) & lebih nyaman bertransaksi di cabang.")
        st.markdown(
            "- Berikan insentif *cashback* untuk transaksi pertama via mobile banking.\n"
            "- Sediakan pendampingan aktivasi digital saat nasabah berkunjung ke cabang.\n"
            "- Tawarkan cicilan 0% untuk transaksi ritel bulanan."
        )

with col3:
    with st.container(border=True):
        st.markdown("### 📞 Segmen Rendah")
        st.caption("Limit kecil (~$12.100) & intensitas panggilan ke CS paling tinggi.")
        st.markdown(
            "- Perkuat fitur chatbot & pusat bantuan mandiri di aplikasi untuk menekan biaya operasional CS.\n"
            "- Kirim edukasi pengelolaan tagihan dan pengingat jatuh tempo otomatis."
        )