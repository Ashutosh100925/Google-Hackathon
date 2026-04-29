import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Path setup
root_dir = os.path.dirname(__file__)
backend_dir = os.path.join(root_dir, "api", "backend_src")
ai_dir = os.path.join(root_dir, "api", "ai_src")

# Add paths to sys.path so routers can find their services
sys.path.insert(0, backend_dir)
sys.path.insert(0, ai_dir)
sys.path.insert(0, root_dir)

# Import routers from the consolidated backend_src
try:
    from routers import health, analyze
except ImportError:
    # If standard import fails, try relative to backend_dir
    sys.path.append(backend_dir)
    from routers import health, analyze

# Explicit FastAPI instance for Vercel detection
app = FastAPI(
    title="FairAI API",
    description="Backend API for the FairAI Decision Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unified Router for Vercel
from fastapi import APIRouter
from services.ml_service import run_prediction

# Unified Router for Vercel (without prefix here)
api_router = APIRouter()

@api_router.get("/analyze")
async def analyze_get_info():
    return {"success": False, "error": "Method Not Allowed. Please use POST for analysis."}

@api_router.post("/analyze")
@api_router.post("/analyze/")
async def analyze_data_direct(request: analyze.AnalysisRequestPayload):
    try:
        return run_prediction(request.model_type, request.features)
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={"success": False, "error": str(e), "detail": traceback.format_exc()})

@api_router.get("/health")
@api_router.get("/health/")
async def health_direct():
    return {"status": "ok", "message": "FairAI API is up and running."}

@api_router.get("/debug-routes")
def debug_routes():
    return {"routes": [{"path": r.path, "methods": list(r.methods) if hasattr(r, "methods") else []} for r in app.routes]}

@api_router.get("/firebase-config")
async def get_firebase_config():
    """
    Returns the Firebase configuration from environment variables.
    """
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID")
    }

@api_router.get("/firebase-config-js")
async def get_firebase_config_js():
    """
    Returns the Firebase configuration as a Javascript file.
    This allows us to load it synchronously in index.html.
    """
    config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID")
    }
    import json
    js_content = f"window.firebaseConfig = {json.dumps(config)};"
    from fastapi.responses import Response
    return Response(content=js_content, media_type="application/javascript")

# Include the router twice to handle both prefixed and non-prefixed paths
app.include_router(api_router, prefix="/api")
app.include_router(api_router)

@app.get("/{path:path}")
def catch_all(path: str):
    return JSONResponse(status_code=404, content={"success": False, "error": f"Path not found: /{path}"})

from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import traceback
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "detail": traceback.format_exc() if not os.environ.get("VERCEL") else "Internal Server Error"
        }
    )
