import os, random
import streamlit as st
from dotenv import load_dotenv
from backend.i18n import t, TRANSLATIONS
from backend.security import generate_otp, issue_token
from backend import data_access as dao
import pandas as pd

load_dotenv()
st.set_page_config(page_title="ERP Chatbot Advanced", page_icon="🤖")

# Session init
if "otp" not in st.session_state: st.session_state.otp = None
if "session" not in st.session_state: st.session_state.session = None
if "member_id" not in st.session_state: st.session_state.member_id = None
if "lang" not in st.session_state: st.session_state.lang = "en"

# Language toggle
lang = st.sidebar.selectbox(TRANSLATIONS['en']['lang_label'] + " / " + TRANSLATIONS['ur']['lang_label'], ["en", "ur"], index=0)
st.session_state.lang = lang

st.title("🤖 " + t(lang, "welcome_title"))

# Login / OTP
member_ids = list(dao.load_members().keys())
member_choice = st.selectbox(t(lang, "select_member"), options=[""] + member_ids)
phone_input = st.text_input("Phone (demo)", value="")
if st.button(t(lang, "send_otp")):
    if member_choice and phone_input:
        # In production: validate phone matches member
        st.session_state.otp = generate_otp()
        st.info(f"Demo OTP (for testing): {st.session_state.otp}")
    else:
        st.warning("Select member and enter phone.")

otp_entered = st.text_input(t(lang, "enter_otp"))
if st.button(t(lang, "verify")):
    if otp_entered and otp_entered == st.session_state.otp:
        st.session_state.member_id = member_choice
        # Role: make M001 admin in demo
        role = "admin" if member_choice == "M001" else "member"
        st.session_state.session = issue_token(member_choice, role=role)
        st.success("Logged in.")
    else:
        st.error("Invalid OTP.")

# If logged in
if st.session_state.session:
    m = dao.get_member(st.session_state.member_id)
    st.write(f"**{m['name']}** ({st.session_state.member_id}) — {m['status']}")

    option = st.radio(t(lang, "menu_title"), [
        t(lang, "opt_status"),
        t(lang, "opt_fees"),
        t(lang, "opt_events"),
        t(lang, "opt_certificate"),
        t(lang, "opt_forms"),
    ])

    # Membership Status
    if option == t(lang, "opt_status"):
        st.info(t(lang, "status_msg", status=m["status"], date=m["renewal_date"]))

    # Pending Fees
    if option == t(lang, "opt_fees"):
        st.warning(t(lang, "fees_msg", amount=m["pending_fees"], date=m["renewal_date"]))

    # Events
    if option == t(lang, "opt_events"):
        st.subheader("📅 " + t(lang, "events_title"))
        for e in dao.load_events():
            st.write(f"- {e['date']}: {e['title']}")

    # Certificate
    if option == t(lang, "opt_certificate"):
        out_pdf = os.path.join("certificates", f"{st.session_state.member_id}_certificate.pdf")
        os.makedirs("certificates", exist_ok=True)
        dao.generate_certificate(st.session_state.member_id, out_pdf)
        st.success(t(lang, "certificate_ready"))
        st.download_button("📄 Download", data=open(out_pdf, "rb"), file_name=os.path.basename(out_pdf))

    # Automated Form Filling
    if option == t(lang, "opt_forms"):
        st.subheader(t(lang, "form_title"))
        new_name = st.text_input(t(lang, "form_name"), value=m["name"])
        new_phone = st.text_input(t(lang, "form_phone"), value=m["phone"])
        if st.button(t(lang, "form_save")):
            m["name"], m["phone"] = new_name, new_phone
            dao.save_member(st.session_state.member_id, m)
            st.success(t(lang, "form_saved"))

    # Interaction log (demo)
    os.makedirs("logs", exist_ok=True)
    row = {
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "member_id": st.session_state.member_id,
        "option": option,
        "lang": lang
    }
    log_path = os.path.join("logs", "interactions.csv")
    if os.path.exists(log_path):
        df = pd.read_csv(log_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(log_path, index=False)

    if st.button(t(lang, "logout")):
        st.session_state.clear()
        st.experimental_rerun()