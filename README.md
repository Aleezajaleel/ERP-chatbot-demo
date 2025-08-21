# ERP Chatbot Advanced (Demo) 🤖

A professional, menu-driven chatbot demo for **Islamabad Chamber**, designed to connect to Oracle ERP (simulated with local files). Includes multilingual (Urdu/English), OTP login (demo), role-based access, document generation, and an admin dashboard.

## Features
- **Menu-driven UX** (no personal data typing; select options)
- **Live-style data fetch** from simulated ERP (easily switchable to Oracle)
- **Urdu & English** with instant toggle
- **OTP login (demo)** with role-based access (M001 is Admin)
- **Document Search & Retrieval** (auto-generate membership certificate PDF)
- **Automated Form Filling** (updates persist in demo DB)
- **Admin Dashboard** (logs interactions)
- **WhatsApp Integration**: architecture & placeholder notes

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open your browser at http://localhost:8501

**Demo Login:** Select `M001` or `M002`, enter any phone, click *Send OTP* (OTP will display on screen), then *Verify*.

## Connect to Oracle (Production)
- Replace file-based `backend/data_access.py` with Oracle queries using `python-oracledb` or REST APIs.
- Use environment variables in `.env` (DSN, USER, PASS).
- Enforce real authentication (SSO/OTP via SMS provider).

## WhatsApp (Production Path)
See `utils/whatsapp_placeholder.md`. Use Business API (Twilio/360dialog), map phone → Member ID, reuse the same backend functions.

## Structure
```
ERP-Chatbot-Advanced/
├─ app.py
├─ pages/1_Admin_Dashboard.py
├─ backend/
│  ├─ data_access.py
│  ├─ i18n.py
│  └─ security.py
├─ data/
│  ├─ members.json
│  └─ events.json
├─ certificates/
├─ logs/
├─ utils/whatsapp_placeholder.md
├─ assets/
├─ .env
└─ requirements.txt
```

## Notebook
A walkthrough notebook is provided at `demo_walkthrough.ipynb` with explanations.