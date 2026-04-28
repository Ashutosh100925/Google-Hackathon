import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from services.ml_service import extract_features, run_prediction

print("--- Testing Amit Das ---")
amit = {
    "Name": "Amit Das",
    "Age": 24,
    "Gender": "Male",
    "Education": "Bachelor's in Arts",
    "Experience": "1 year",
    "Technical Skills": "Basic Excel, HTML",
    "Performance History": "Below expectations",
    "Communication": "Poor",
    "City Tier": "Tier 3"
}
print(extract_features(amit))
res_amit = run_prediction("hiring", amit)
print(res_amit["decision"], res_amit["confidence_score"])


print("\n--- Testing Rahul Verma ---")
rahul = {
    "Name": "Rahul Verma",
    "Age": 30,
    "Gender": "Male",
    "Education": "Master's in Computer Science",
    "Experience": "6 years",
    "Technical Skills": "Python, FastAPI, AWS, Docker, SQL",
    "Performance History": "Exceeded expectations",
    "Communication": "Good",
    "City Tier": "Tier 1"
}
print(extract_features(rahul))
res_rahul = run_prediction("hiring", rahul)
print(res_rahul["decision"], res_rahul["confidence_score"])
