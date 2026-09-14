from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin._auth_utils import EmailAlreadyExistsError
import os
import requests
from dotenv import load_dotenv

load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
app = FastAPI()

# Firebase connection
cred = credentials.Certificate("fashion-app-4c7bd-firebase-adminsdk-fbsvc-e0261e1e64.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


class UserSignup(BaseModel):
    name: str
    email: str
    password: str


class AnalyzeRequest(BaseModel):
    image_url: str
    dress: str
    footwear: str
    makeup: str
    jewelry: str


@app.get("/")
def home():
    return {
        "message": "Fashion App Backend is running!"
    }


@app.post("/signup")
def signup(user: UserSignup):

    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )

        db.collection("users").add({
            "name": user.name,
            "email": user.email
        })

        return {"message": "User created successfully"}

    except EmailAlreadyExistsError:
        return {"message": "Email already registered"}

    except ValueError as e:
        return {"message": str(e)}


@app.post("/login")
def login(user: UserSignup):

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    response = requests.post(
        url,
        json={
            "email": user.email,
            "password": user.password,
            "returnSecureToken": True
        }
    )

    if response.status_code == 200:
        data = response.json()

        return {
            "message": "Login successful",
            "email": data["email"],
            "idToken": data["idToken"]
        }

    return {
        "message": "Invalid email or password"
    }

@app.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    db.collection("uploads").add({
        "filename": file.filename,
        "path": file_path
    })

    return {
        "message": "Photo uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }


@app.post("/analyze")
def analyze_outfit(data: AnalyzeRequest):

    result = {
        "image_url": data.image_url,
        "dress": data.dress,
        "footwear": data.footwear,
        "makeup": data.makeup,
        "jewelry": data.jewelry,
        "match_score": 85,
        "color_harmony": "Good",
        "style_compatibility": "Excellent",
        "occasion_suitability": "Suitable for party"
    }

    db.collection("outfit_results").add(result)

    return {
        "message": "Outfit analysis saved successfully",
        **result
    }
@app.get("/users")
def get_users():
    users = db.collection("users").stream()

    return [
        {
            "id": user.id,
            **user.to_dict()
        }
        for user in users
    ]
class RFIDRequest(BaseModel):
    uid: str


@app.post("/wardrobe/rfid")
def add_rfid_clothing(data: RFIDRequest):

    clothing = {
        "01:02:03:04": "Black T-Shirt",
        "11:22:33:44": "Blue Jeans",
        "55:66:77:88": "Red Dress"
    }

    item = clothing.get(data.uid, "Unknown Clothing")

    db.collection("wardrobe").add({
        "rfid_uid": data.uid,
        "clothing": item
    })

    return {
        "message": "Clothing added to wardrobe",
        "rfid_uid": data.uid,
        "clothing": item
    }
