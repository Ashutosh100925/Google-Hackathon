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
app.include_router(health.router)
app.include_router(analyze.router)

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/", status_code=307)
