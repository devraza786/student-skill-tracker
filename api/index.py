import os
import sys
import json

# Isolation Mode Diagnostic (No Imports)
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
            ]
        })
        await send({'type': 'http.response.body', 'body': b''})
        return

    # Success Response (Isolation Mode)
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'application/json'),
            (b'access-control-allow-origin', b'*'),
        ]
    })
    
    diag_data = {
        "status": "ISOLATION_MODE_ACTIVE",
        "location": "REPO_ROOT",
        "message": "If you see this, Vercel is successfully reaching the ROOT entry point.",
        "cwd": os.getcwd(),
        "sys_path": sys.path,
        "env_keys": list(os.environ.keys())
    }
    await send({
        'type': 'http.response.body',
        'body': json.dumps(diag_data).encode('utf-8')
    })
