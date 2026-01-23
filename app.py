from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Wine Quality Inference API")

model = joblib.load("model.pkl")

class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    chlorides: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.post("/predict")
def predict(data: WineInput):
    features = np.array([[
        data.fixed_acidity,
        data.volatile_acidity,
        data.chlorides,
        data.total_sulfur_dioxide,
        data.density,
        data.pH,
        data.sulphates,
        data.alcohol
    ]])

    pred = model.predict(features)[0]

    return {
        "name": "S Varun Balaji",
        "roll_no": "2022BCS0152",
        "wine_quality": round(float(pred))
    }
