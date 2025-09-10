# src/app.py
import joblib
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import jwt, os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load secrets
load_dotenv("../.env")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")

# Load ML model + vectorizer
vectorizer = joblib.load("../models/vectorizer.joblib")
model = joblib.load("../models/model.joblib")


app = FastAPI(title="Smart Symptom Triage API")

# ---------- Auth ----------
def create_token(user: str):
    payload = {
        "sub": user,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(authorization: str = Header(None)):
    """
    ✅ Fixed verification:
    - Accepts both "Bearer <token>" and raw token
    - Works with Swagger, Thunder Client, curl
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        # Handle "Bearer <token>" or just token
        if authorization.lower().startswith("bearer "):
            token = authorization.split(" ")[1]
        else:
            token = authorization.strip()

        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------- Schemas ----------
class SymptomInput(BaseModel):
    text: str

class TokenRequest(BaseModel):
    username: str

# ---------- Routes ----------
@app.post("/get-token")
def get_token(req: TokenRequest):
    token = create_token(req.username)
    return {"token": token}

@app.post("/predict")
def predict(symptom: SymptomInput, user=Depends(verify_token)):
    X = vectorizer.transform([symptom.text])
    pred = model.predict(X)[0]
    return {"prediction": pred}

# ---------- Run locally ----------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
