import os
import sys
import traceback
import json

# Minimal dependency-free WSGI app for diagnostics
def app(environ, start_response):
    try:
        # 1. Adjust Path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if base_dir not in sys.path:
            sys.path.append(base_dir)
        
        # 2. Try to Import the real app
        from app.main import app as real_app
        
        # 3. If we get here, the import worked!
        # For simplicity, we'll just report success or handle the request if it's an ASGI app
        # Vercel handles ASGI/WSGI automatically if assigned to 'app'
        return real_app(environ, start_response)

    except Exception as e:
        # Something failed during boot
        status = '500 Internal Server Error'
        headers = [
            ('Content-type', 'application/json'),
            ('Access-Control-Allow-Origin', '*')
        ]
        start_response(status, headers)
        
        error_data = {
            "diag_status": "CRASH_DURING_IMPORT",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "cwd": os.getcwd(),
            "sys_path": sys.path,
            "root_files": os.listdir('.') if os.path.exists('.') else "os_error"
        }
        return [json.dumps(error_data).encode('utf-8')]
