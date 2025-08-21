import os, secrets, time
from dataclasses import dataclass

@dataclass
class Session:
    member_id: str
    role: str  # 'member' or 'admin'
    token: str
    issued_at: float

def generate_otp():
    return f"{secrets.randbelow(10**6):06d}"

def issue_token(member_id, role='member'):
    token = secrets.token_hex(16)
    return Session(member_id=member_id, role=role, token=token, issued_at=time.time())

def has_role(session, role):
    return session and session.role == role