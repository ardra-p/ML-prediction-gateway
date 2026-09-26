import httpx
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
import os

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://localhost:8001")

app = FastAPI()

class PredictRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Text message to classify")

@app.post("/predict")
async def predict(request: PredictRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MODEL_SERVICE_URL}/predict",
                json={"message": request.message},
                timeout=5.0
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Model service unavailable")

    return response.json()