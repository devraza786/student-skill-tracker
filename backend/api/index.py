import os
import sys
import traceback

try:
    # Ensure the parent directory is in the path so we can import 'app'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.append(base_dir)
    
    from app.main import app
except Exception as e:
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/{path:path}")
    async def catch_all(path: str = None):
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "cwd": os.getcwd(),
            "sys_path": sys.path
        }

    @app.get("/")
    async def root_error():
        # Using a direct call to the generic catch_all logic
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "cwd": os.getcwd(),
            "sys_path": sys.path
        }
