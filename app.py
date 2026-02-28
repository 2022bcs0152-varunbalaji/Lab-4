from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path

app = FastAPI(title="Wine Quality Inference API")

MODEL_PATH = Path("model.pkl")
_model = None
_model_load_error = None

try:
    if MODEL_PATH.exists():
        _model = joblib.load(str(MODEL_PATH))
    else:
        _model_load_error = f"Model file not found: {MODEL_PATH.resolve()}"
except Exception as exc:  # noqa: BLE001
    _model_load_error = str(exc)

class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.get("/health")
def health():
    if _model is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "model_loaded": False,
                "error": _model_load_error,
            },
        )
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(data: WineInput):
    if _model is None:
        raise HTTPException(status_code=503, detail=f"Model not loaded: {_model_load_error}")

    features = np.array([[
        data.fixed_acidity,
        data.volatile_acidity,
        data.citric_acid,
        data.residual_sugar,
        data.chlorides,
        data.free_sulfur_dioxide,
        data.total_sulfur_dioxide,
        data.density,
        data.pH,
        data.sulphates,
        data.alcohol
    ]])

    pred = _model.predict(features)[0]

    return {
        "name": "S Varun Balaji",
        "roll_no": "2022BCS0152",
        "wine_quality": round(float(pred))
    }
