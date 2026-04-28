from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from services.ml_service import run_prediction

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

class AnalysisRequestPayload(BaseModel):
    model_type: str
    features: Dict[str, Any]

@router.post("/")
async def analyze_data(request: AnalysisRequestPayload):
    """
    Base route for analysis.
    Accepts JSON payload with model_type (hiring, loan, admission) and features.
    """
    try:
        # Phase 2 ML Prediction Execution
        ml_results = run_prediction(request.model_type, request.features)
        
        result = {
            "status": "success",
            "model_type": request.model_type,
            # Backward compatible bindings
            "prediction": ml_results["prediction"],
            "confidence": ml_results["confidence"],
            "feature_importance": ml_results["feature_importance"],
            "formatted_confidence": ml_results["explanation_data"]["formatted_confidence"],
            "structured_features": request.features,
            
            # Step 10 Exact Bindings
            "decision": ml_results["decision"],
            "confidence_score": ml_results["confidence_score"],
            "bias_detected": ml_results["bias_detected"],
            "fairness_score": ml_results["fairness_score"],
            "top_factors": ml_results["top_factors"],
            "negative_factors": ml_results["negative_factors"],
            "rule_override": ml_results["rule_override"],
            "explanation": ml_results["explanation_data"]["explanation_text"],
            "decision_sensitivity": ml_results["explanation_data"]["decision_sensitivity"],
            "recommendation": ml_results["explanation_data"]["recommendation"],
            "risk_level": ml_results["risk_level"],
            "bias_report": ml_results["bias_report"]
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/what-if")
async def what_if_analysis(request: AnalysisRequestPayload):
    """
    Sub-route for real-time what-if simulation workflows.
    Accepts tweaked features generated from the frontend sliders and returns stripped down predictions.
    """
    try:
        # Re-run ML Prediction Execution based on mutated features
        ml_results = run_prediction(request.model_type, request.features)
        
        result = {
            "status": "success",
            "decision": ml_results["prediction"],
            "confidence_score": ml_results["confidence"] * 100, 
            "fairness_score": ml_results["fairness_metrics"]["demographic_parity"] * 100 
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-If Analysis failed: {str(e)}")

@router.post("/document")
async def analyze_document(
    model_type: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Route for document based analysis (e.g., CSV, JSON, TXT).
    Parses the file and extracts numerical features securely.
    """
    import io
    import csv
    
    try:
        content = await file.read()
        filename = file.filename.lower()
        features = {}

        # Parsing & Validation Routing
        if filename.endswith(".json"):
            try:
                features = json.loads(content.decode('utf-8'))
            except Exception:
                raise ValueError("Invalid Error: Uploaded JSON could not be parsed.")
                
        elif filename.endswith(".csv"):
            try:
                decoded = content.decode('utf-8')
                reader = csv.DictReader(io.StringIO(decoded))
                row = next(reader, None)
                if not row:
                    raise ValueError("Validation Error: CSV file contains no structured data rows.")
                features = dict(row)
            except Exception:
                raise ValueError("Invalid Error: Uploaded CSV could not be parsed.")
                
        elif filename.endswith(".txt"):
            # Robust extraction of generic text into numeric metrics to prevent null matrices
            text = content.decode('utf-8')
            features = {
                "text_density": len(text),
                "complexity_score": len(text.split()),
                "domain_relevance": (len(text) % 10) + 1
            }
        else:
            raise ValueError(f"Format Validation Error: {filename} is not supported. Please use CSV, JSON, or TXT.")

        # Real-time inference
        ml_results = run_prediction(model_type, features)
        
        result = {
            "status": "success",
            "model_type": model_type,
            "filename": file.filename,
            # Backward compatible bindings
            "prediction": ml_results["prediction"],
            "confidence": ml_results["confidence"],
            "feature_importance": ml_results["feature_importance"],
            "formatted_confidence": ml_results["explanation_data"]["formatted_confidence"],
            "structured_features": features,

            # Step 10 Exact Bindings
            "decision": ml_results["decision"],
            "confidence_score": ml_results["confidence_score"],
            "bias_detected": ml_results["bias_detected"],
            "fairness_score": ml_results["fairness_score"],
            "top_factors": ml_results["top_factors"],
            "negative_factors": ml_results["negative_factors"],
            "rule_override": ml_results["rule_override"],
            "explanation": ml_results["explanation_data"]["explanation_text"],
            "decision_sensitivity": ml_results["explanation_data"]["decision_sensitivity"],
            "recommendation": ml_results["explanation_data"]["recommendation"],
            "risk_level": ml_results["risk_level"],
            "bias_report": ml_results["bias_report"]
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")
