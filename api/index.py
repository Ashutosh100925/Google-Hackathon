import importlib.util
import os
import sys


def _load_backend_app():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    backend_dir = os.path.join(repo_root, "3D Web.0", "GDG", "backend")
    shared_dir = os.path.join(repo_root, "3D Web.0", "GDG")

    # Allow `from routers import ...` and importing `unbiased_ai_system`
    sys.path.insert(0, backend_dir)
    sys.path.insert(0, shared_dir)

    backend_app_path = os.path.join(backend_dir, "app.py")
    spec = importlib.util.spec_from_file_location("fairai_backend_app", backend_app_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load backend FastAPI app module.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    if not hasattr(module, "app"):
        raise RuntimeError("Backend module does not expose `app`.")
    return module.app


app = _load_backend_app()

