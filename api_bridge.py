import os
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

def get_readonly_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    if hasattr(st, "secrets") and "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    raise ValueError("Holding veri köprüsü yetkilendirilemedi (Secrets eksik).")

@st.cache_data(ttl=600, show_spinner=False)
def fetch_global_trade_macro():
    try:
        client = get_readonly_client()
        # OZ Global Trade Tablo ID'si
        sheet = client.open_by_key("1uNEFwXCZgfjmg6V49cOKGfLiM5h-JhnKu1b0n494ZEg")
        
        # Sadece ciro ve kargo özeti için gerekli minimal okuma
        managers = ["EREN MEMİŞOĞLU", "BEYZA YAZAR", "EREN ZORMAN", "ZERRİN ÖZ"]
        toplam_ciro = 0.0
        toplam_kar = 0.0
        
        for mgr in managers:
            try:
                ws = sheet.worksheet(mgr)
                vals = ws.get_all_values()
                for row in vals[5:25]:
                    if len(row) >= 15 and row[0].strip() != "" and row[0].strip() != "Örnek":
                        satis = str(row[12]).replace("$", "").replace(",", "").strip()
                        kar = str(row[14]).replace("$", "").replace(",", "").strip() if len(row) > 14 else "0"
                        if satis.replace(".", "").isdigit(): toplam_ciro += float(satis)
                        if kar.replace(".", "").isdigit() or (kar.startswith("-") and kar[1:].replace(".", "").isdigit()): toplam_kar += float(kar)
            except:
                continue
                
        try:
            ws_crg = sheet.worksheet("KARGOLAR")
            aktif_kargolar = len([r for r in ws_crg.get_all_values()[1:] if r and len(r) > 6 and "TESLİM" not in str(r[6]).upper()])
        except:
            aktif_kargolar = 0

        return {
            "toplam_ciro": toplam_ciro,
            "toplam_kar": toplam_kar,
            "marj": (toplam_kar / toplam_ciro * 100) if toplam_ciro > 0 else 0,
            "aktif_kargo": aktif_kargolar
        }
    except Exception as e:
        return {"hata": str(e)}

@st.cache_data(ttl=600, show_spinner=False)
def fetch_sutlu_kavurma_macro():
    # Sütlü Kavurma entegrasyonu tamamlandığında bura Adisyo API'ye bağlanacak
    return {
        "aylik_ciro": 0.0,
        "net_nakit": 0.0,
        "bekleyen_borc": 0.0
    }
