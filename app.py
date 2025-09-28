import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime

st.title("📓 รายงานประจำวันเกี่ยวกับคดี Sirius Dawn")

# --- โหลด credentials จากไฟล์ JSON ---
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# --- เปิดไฟล์และชีท ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/10F4lPyLDCBS2Lkug6FCp8D0LT89YIFLJrPOLFvs0umo/edit#gid=0"
sheet = client.open_by_url(SHEET_URL).worksheet("Sheet1")

# ---- ฟอร์มบันทึก ----
with st.form("daily_form", clear_on_submit=True):
    number = st.number_input("ลำดับ", min_value=1, step=1)
    report_date = st.date_input("วันที่", value=date.today())
    report_time = st.text_input(
        "เวลา (HH:MM)",
        value=datetime.now().strftime("%H:%M"),
        help="ใส่เวลาแบบ 24 ชั่วโมง เช่น 09:30 หรือ 15:45"
    )
    detail = st.text_area("รายการ", height=120)
    submitted = st.form_submit_button("บันทึก")

if submitted:
    try:
        valid_time = datetime.strptime(report_time, "%H:%M").strftime("%H:%M")
        sheet.append_row([
            number,
            report_date.strftime("%d/%m/%Y"),
            valid_time,
            detail
        ])
        st.success("✅ บันทึกลง Google Sheets แล้ว")
    except ValueError:
        st.error("❌ รูปแบบเวลาไม่ถูกต้อง! กรุณาใส่เป็น HH:MM เช่น 09:30")

# ---- แสดงข้อมูลจาก Sheets ----
data = sheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)
else:
    st.info("ยังไม่มีข้อมูล")
