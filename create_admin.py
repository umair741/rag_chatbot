# create_admin.py
from db import SessionLocal
import models
from security import hash_password
import os

db = SessionLocal()

ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

existing_admin = db.query(models.User).filter(models.User.email == ADMIN_EMAIL).first()
if existing_admin:
    print(f"Admin already exists: {existing_admin.email}")
else:
    new_admin = models.User(
        name=ADMIN_NAME,
        email=ADMIN_EMAIL,
        password=hash_password(ADMIN_PASSWORD),
        role="admin"
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    print(f"Admin created successfully: {new_admin.email}")

db.close()
