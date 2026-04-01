import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_super_secret_jwt_key_here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def generate_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

if __name__ == "__main__":
    admin_token = generate_token("admin_user", "system admin")
    regular_user_token = generate_token("regular_user", "user")
    
    print("--- SYSTEM ADMIN TOKEN ---")
    print(admin_token)
    print("\n--- REGULAR USER TOKEN ---")
    print(regular_user_token)
