import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, Birch
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from model_utils import load_data, FITUR

st.title("Lab Eksplorasi Data & Evaluasi Model")
df = load_data()
k = st.session_state.get("k_selected", 3)

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Inspeksi & Distribusi Data",
    "2. Preprocessing & Skala",
    "3. Proyeksi PCA 2D",
    "4. Komparasi Algoritma",
])

with tab1:
    c1, c2 = st.columns([1.2, 1])
    with c1:
        fitur_pilih = st.selectbox("Pilih variabel untuk dianalisis:", FITUR)
        fig, ax = plt.subplots(figsize=(6, 3.6))
        sns.histplot(df[fitur_pilih], kde=True, ax=ax, color="#0f766e")
        ax.set_title(f"Sebaran Nilai {fitur_pilih}")
        st.pyplot(fig)
    with c2:
        fig_corr, ax_corr = plt.subplots(figsize=(5, 3.8))
        sns.heatmap(df[FITUR].corr(), annot=True, cmap="GnBu", fmt=".2f", ax=ax_corr)
        ax_corr.set_title("Korelasi Antar Fitur")
        st.pyplot(fig_corr)
    with st.expander("Lihat Sampel Data Mentah (20 Baris Pertama)"):
        st.dataframe(df.head(20), use_container_width=True)

with tab2:
    st.markdown(
        "Kolom identitas (`Sl_No`, `Customer Key`) dieliminasi dan seluruh fitur numerik "
        "dinormalisasi menggunakan `StandardScaler` agar fitur bernilai besar tidak mendominasi jarak Euclidean."
    )
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df[FITUR]), columns=FITUR)
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("Sebelum Standardisasi")
        st.dataframe(df[FITUR].describe().loc[["mean", "std", "min", "max"]].round(2), use_container_width=True)
    with col_b:
        st.caption("Sesudah Standardisasi")
        st.dataframe(df_scaled.describe().loc[["mean", "std", "min", "max"]].round(2), use_container_width=True)

with tab3:
    X_scaled = StandardScaler().fit_transform(df[FITUR])
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    labels_pca = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X_scaled)

    m1, m2, m3 = st.columns(3)
    m1.metric("Varians PC1", f"{pca.explained_variance_ratio_[0]*100:.2f}%")
    m2.metric("Varians PC2", f"{pca.explained_variance_ratio_[1]*100:.2f}%")
    m3.metric("Total Informasi Terjaga", f"{sum(pca.explained_variance_ratio_)*100:.2f}%")

    fig_p, ax_p = plt.subplots(figsize=(8, 4))
    sc = ax_p.scatter(X_pca[:, 0], X_pca[:, 1], c=labels_pca, cmap="viridis", alpha=0.8)
    ax_p.set_xlabel("Principal Component 1")
    ax_p.set_ylabel("Principal Component 2")
    ax_p.set_title(f"Pemetaan Klaster pada Ruang PCA 2D (k = {k})")
    plt.colorbar(sc, ax=ax_p, label="ID Klaster")
    st.pyplot(fig_p)

with tab4:
    st.caption(f"Menggunakan jumlah klaster k = {k} (ubah nilai k melalui slider di sidebar kiri).")
    X_scaled = StandardScaler().fit_transform(df[FITUR])
    algoritma = {
        "K-Means": KMeans(n_clusters=k, random_state=42, n_init=10),
        "Agglomerative": AgglomerativeClustering(n_clusters=k),
        "Gaussian Mixture": GaussianMixture(n_components=k, random_state=42),
        "BIRCH": Birch(n_clusters=k),
    }
    rows = []
    for nama, mdl in algoritma.items():
        lbl = mdl.fit_predict(X_scaled)
        rows.append({
            "Algoritma": nama,
            "Silhouette Score (↑)": round(silhouette_score(X_scaled, lbl), 4),
            "Davies-Bouldin Index (↓)": round(davies_bouldin_score(X_scaled, lbl), 4),
            "Calinski-Harabasz (↑)": round(calinski_harabasz_score(X_scaled, lbl), 2),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)