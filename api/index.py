import os
import sys

# Add necessary paths to sys.path
# Since Vercel runs this from the api/ directory, __file__ is /var/task/api/index.py
api_dir = os.path.dirname(__file__)
backend_dir = os.path.join(api_dir, "backend_src")
ai_dir = os.path.join(api_dir, "ai_src")
repo_root = os.path.abspath(os.path.join(api_dir, ".."))

# Ensure our local modules are found first
sys.path.insert(0, backend_dir)
sys.path.insert(0, ai_dir)
sys.path.insert(0, repo_root)

# Static import for better Vercel static analysis and reliability
try:
    from fairai_app import app
except ImportError as e:
    # Fallback to dynamic load if static fails for some reason (though it shouldn't)
    import importlib.util
    backend_app_path = os.path.join(backend_dir, "fairai_app.py")
    spec = importlib.util.spec_from_file_location("fairai_backend_app", backend_app_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        app = getattr(module, "app")
    else:
        raise e

# The app variable is now exposed to Vercel
