from db import engine, Base  # jahan aapka Base aur engine hai
import models  # jahan aapke User aur ChatHistory classes hain

# Ye line tables ko DB me create karegi agar wo already nahi hain
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully")
