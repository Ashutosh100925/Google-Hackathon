import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Path setup
api_dir = os.path.dirname(__file__)
backend_dir = os.path.join(api_dir, "backend_src")
ai_dir = os.path.join(api_dir, "ai_src")
repo_root = os.path.abspath(os.path.join(api_dir, ".."))

# Add paths to sys.path so routers can find their services
sys.path.insert(0, backend_dir)
sys.path.insert(0, ai_dir)
sys.path.insert(0, repo_root)

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

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")

@app.get("/", include_in_schema=False)
def root_info():
    return {"status": "FairAI API is running", "endpoints": ["/analyze", "/health"]}

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
