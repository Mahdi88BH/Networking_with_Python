from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_and_verify_jwt():
    now = datetime.now(timezone.utc)
    
    # 1. Construct payload with standard JWT registered claims (iat, exp) + custom data
    payload = {
        "sender": "Python JWT",
        "message": "Testing Python JWT",
        "sub": "user_12345",
        "iat": now,
        "exp": now + timedelta(minutes=15)  # Token valid for 15 minutes
    }

    # 2. Encode token
    encoded_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[+] Encoded JWT Token:\n{encoded_token}\n")

    # 3. Decode and verify token
    try:
        # Note: algorithms argument passed as a list ['HS256']
        decoded_payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("[+] Decoded Payload Successfully:")
        for key, value in decoded_payload.items():
            print(f"  - {key:<10}: {value}")

    except jwt.ExpiredSignatureError:
        print("[-] Verification Failed: The token signature has expired.")
    except jwt.InvalidTokenError as err:
        print(f"[-] Verification Failed: Invalid token ({err})")

if __name__ == "__main__":
    create_and_verify_jwt()