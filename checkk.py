from db import get_db
from sqlalchemy import text

db = next(get_db())
result = db.execute(text("SELECT 1")).fetchall()
print(result)
