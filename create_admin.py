# create_admin.py
from db import SessionLocal
import models
from security import hash_password

db = SessionLocal()

ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "StrongP@ssw0rd!"  # Must satisfy your password rules

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
