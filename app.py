import streamlit as st
import plotly.express as px
import pandas as pd
from api_bridge import fetch_global_trade_macro, fetch_sutlu_kavurma_macro

st.set_page_config(page_title="OZ GROUP — Yönetim Kurulu", page_icon="🏢", layout="wide")

st.title("🏢 OZ GROUP — Konsolide Yönetim Paneli")
st.markdown("*(Zero Trust Mimarisi — Salt Okunur Konsolidasyon Ağı)*")
st.divider()

# API Köprülerinden Veri Çekimi
with st.spinner("Alt şirket bağlantıları (API Bridge) sorgulanıyor..."):
    ogt_metrics = fetch_global_trade_macro()
    sk_metrics = fetch_sutlu_kavurma_macro()

# Üst Düzey Yönetim Metrikleri
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌐 OZ GLOBAL TRADE")
    if "hata" in ogt_metrics:
        st.error("Veri köprüsü hatası: Bağlantı kurulamadı.")
    else:
        mc1, mc2 = st.columns(2)
        mc1.metric("Toplam Dış Ticaret Hacmi", f"${ogt_metrics['toplam_ciro']:,.0f}")
        mc2.metric("Brüt Kâr", f"${ogt_metrics['toplam_kar']:,.0f}", f"%{ogt_metrics['marj']:.1f} Marj")
        st.metric("Yoldaki Aktif Sevkiyatlar", f"{ogt_metrics['aktif_kargo']} Kargo")

with col2:
    st.subheader("🥩 SÜTLÜ KAVURMA RESTORAN")
    # Altyapı kurulana kadar bekleyen statü
    st.info("Adisyo API entegrasyonu bekleniyor...")
    mc3, mc4 = st.columns(2)
    mc3.metric("Aylık Konsolide Ciro", "₺0.00")
    mc4.metric("Net Nakit Akışı", "₺0.00")
