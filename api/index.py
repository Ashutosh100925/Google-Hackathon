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


class ApiPrefixCompatWrapper:
    """
    Vercel rewrite compatibility:
    - Some setups pass /api/... through to this function unchanged
    - Others strip /api and pass /...
    This wrapper supports both by stripping a leading /api before dispatch.
    """

    def __init__(self, asgi_app, prefix="/api"):
        self.asgi_app = asgi_app
        self.prefix = prefix

    async def __call__(self, scope, receive, send):
        if scope.get("type") in {"http", "websocket"}:
            original_path = scope.get("path", "")
            adjusted_path = original_path

            if original_path == self.prefix:
                adjusted_path = "/"
            elif original_path.startswith(f"{self.prefix}/"):
                adjusted_path = original_path[len(self.prefix):]

            if adjusted_path != original_path:
                updated_scope = dict(scope)
                updated_scope["path"] = adjusted_path

                raw_path = scope.get("raw_path")
                if isinstance(raw_path, (bytes, bytearray)):
                    if raw_path == self.prefix.encode():
                        updated_scope["raw_path"] = b"/"
                    elif raw_path.startswith(f"{self.prefix}/".encode()):
                        updated_scope["raw_path"] = raw_path[len(self.prefix):]

                scope = updated_scope

        await self.asgi_app(scope, receive, send)


app = ApiPrefixCompatWrapper(_load_backend_app())

