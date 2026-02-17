import os
import sys
import traceback
import json

# Ensure the backend directory is in the path
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(base_dir), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Try to import from the backend subfolder
    from backend.app.main import app as real_app
    app = real_app
except Exception as boot_error:
    error_trace = traceback.format_exc()
    
    async def app(scope, receive, send):
        if scope['type'] != 'http':
            return

        # Handle CORS Preflight (OPTIONS)
        if scope['method'] == 'OPTIONS':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    (b'access-control-allow-origin', b'*'),
                    (b'access-control-allow-methods', b'*'),
                    (b'access-control-allow-headers', b'*'),
                    (b'access-control-max-age', b'86400'),
                ]
            })
            await send({'type': 'http.response.body', 'body': b''})
            return

        # Handle normal requests with the diagnostic error
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [
                (b'content-type', b'application/json'),
                (b'access-control-allow-origin', b'*'),
            ]
        })
        
        diag_data = {
            "diag_status": "ROOT_CRASH_DURING_IMPORT",
            "error": str(boot_error),
            "type": type(boot_error).__name__,
            "traceback": error_trace,
            "cwd": os.getcwd(),
            "sys_path": sys.path,
            "backend_dir_exists": os.path.exists(backend_dir),
            "root_files": os.listdir('.') if os.path.exists('.') else "os_error"
        }
        await send({
            'type': 'http.response.body',
            'body': json.dumps(diag_data).encode('utf-8')
        })
