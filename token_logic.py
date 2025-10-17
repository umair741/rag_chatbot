from fastapi import Request, HTTPException, Depends, status
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "myverysecretkey123"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=5)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(request: Request):
    """
    Checks JWT token from:
    1. Authorization header (API calls)
    2. Cookie (Browser pages)
    Raises HTTPException if no token or invalid token.
    """
    # 1️⃣ Check Authorization header
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    # 2️⃣ Fallback to cookie
    if not token:
        token = request.cookies.get("access_token")

    # 3️⃣ Block if no token
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 4️⃣ Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(current_user: dict = Depends(verify_token)):
    return current_user

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only!")
    return current_user
