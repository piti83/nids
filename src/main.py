import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb

app = FastAPI(
    title="AI-Powered Network Intrusion Detection System (NIDS) API",
    description="Real-time network traffic classification using an optimized XGBoost model.",
    version="1.0"
)

print("Loading XGBoost champion model...")
xgb_model = xgb.XGBClassifier()
xgb_model.load_model('../models/xgboost_v1.json')
print("Model loaded successfully. Ready for inference.")

OPTIMAL_THRESHOLD = 0.9942

class NetworkFlow(BaseModel):
    features: list[float]

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "NIDS API",
        "configured_threshold": OPTIMAL_THRESHOLD
    }

@app.post("/predict")
def predict_traffic(flow: NetworkFlow):
    if len(flow.features) != 40:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid feature count. Expected 40 features, got {len(flow.features)}."
        )
    
    try:
        input_data = np.array(flow.features).reshape(1, -1)
        
        attack_probability = float(xgb_model.predict_proba(input_data)[0, 1])
        
        if attack_probability >= OPTIMAL_THRESHOLD:
            verdict = "ATTACK"
            is_anomaly = True
        else:
            verdict = "BENIGN"
            is_anomaly = False
            
        return {
            "status": "success",
            "attack_probability": round(attack_probability, 6),
            "decision_threshold": OPTIMAL_THRESHOLD,
            "anomaly_detected": is_anomaly,
            "verdict": verdict
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference engine error: {str(e)}")