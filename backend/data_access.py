import json, os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")

def load_members():
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)

def load_events():
    with open(EVENTS_FILE, "r") as f:
        return json.load(f)

def get_member(member_id):
    return load_members().get(member_id)

def save_member(member_id, updated):
    members = load_members()
    members[member_id] = updated
    with open(MEMBERS_FILE, "w") as f:
        json.dump(members, f, indent=2)

def generate_certificate(member_id, out_path):
    m = get_member(member_id)
    if not m: 
        raise ValueError("Member not found")
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-100, "Islamabad Chamber of Commerce")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-140, "Membership Certificate (Demo)")
    c.setFont("Helvetica", 12)
    c.drawString(100, height-200, f"Member ID: {member_id}")
    c.drawString(100, height-220, f"Name: {m['name']}")
    c.drawString(100, height-240, f"Status: {m['status']}")
    c.drawString(100, height-260, f"Renewal Due: {m['renewal_date']}")
    c.drawString(100, height-280, f"Issued: {datetime.now().strftime('%Y-%m-%d')}")
    c.showPage()
    c.save()
    return out_path

# --- Oracle integration placeholder ---
# In production, replace file-based functions with Oracle queries using REST APIs or python-oracledb.
# Example (pseudo):
# import oracledb
# conn = oracledb.connect(dsn=os.getenv('ORACLE_DSN'), user=os.getenv('ORACLE_USER'), password=os.getenv('ORACLE_PASS'))
# cur = conn.cursor()
# cur.execute(\"SELECT * FROM MEMBERS WHERE MEMBER_ID=:id\", id=member_id)
# row = cur.fetchone()