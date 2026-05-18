import joblib
import numpy as np
import requests
import time

API_URL = "http://127.0.0.1:8000/predict"
DATA_PATH = "../data/processed/test_data.joblib"

print("Loading test data for simulation...")
try:
    X_test, y_test = joblib.load(DATA_PATH)
    print("Data loaded successfully!\n")
except FileNotFoundError:
    print(f"ERROR: Could not find the dataset at {DATA_PATH}.")
    exit(1)

y_test_array = np.array(y_test)

benign_indices = np.where(y_test_array == 0)[0]
attack_indices = np.where(y_test_array == 1)[0]

np.random.seed(42) 
selected_benign = np.random.choice(benign_indices, 3, replace=False)
selected_attack = np.random.choice(attack_indices, 3, replace=False)

test_indices = np.concatenate([selected_benign, selected_attack])
np.random.shuffle(test_indices)

print(f"Selected {len(test_indices)} network flow samples for API testing.")
print("Starting simulation...\n")
print("=" * 60)

for idx in test_indices:
    features = X_test.iloc[idx].astype(float).tolist()
    
    actual_label = "ATTACK" if y_test_array[idx] == 1 else "BENIGN"

    payload = {"features": features}

    print(f"Sending flow data... (Ground Truth: {actual_label})")

    start_time = time.time()
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        latency = (time.time() - start_time) * 1000
        
        predicted_verdict = result['verdict']
        probability = result['attack_probability']
        
        print(f"Server Verdict:  {predicted_verdict} (Probability: {probability:.4f})")
        print(f"API Latency:     {latency:.2f} ms")
        
        if actual_label == predicted_verdict:
            print("Status:          [MATCH] - NIDS classified correctly.")
        else:
            print("Status:          [MISMATCH] - NIDS classification error.")
            
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the API.")
        print("Please ensure the FastAPI server is running (uvicorn main:app --reload).")
        break
    except Exception as e:
        print(f"ERROR during API request: {str(e)}")
        
    print("-" * 60)
    time.sleep(1.5)
    
print("Simulation complete.")