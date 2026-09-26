import pickle

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

MODEL_PATH = Path(__file__).parent / "spam_model.pkl"
VECTORIZER_PATH = Path(__file__).parent / "vectorizer.pkl"


model = None
vectorizer = None

@app.on_event("startup")
def load_model():
    global model, vectorizer
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)


class PredictRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Text message to classify")

class PredictResponse(BaseModel):
    label:str
    confidence:float

@app.post("/predict")
def predict(request: PredictRequest):
    X = vectorizer.transform([request.message])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    class_index = list(model.classes_).index(pred)
    confidence = float(proba[class_index])
    return PredictResponse(label=str(pred), confidence=round(confidence, 4))