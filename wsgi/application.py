import os
import sys
from src.main import app
from a2wsgi import ASGIMiddleware

sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'OPTIONS':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']

    wsgi_app = ASGIMiddleware(app)
    return wsgi_app(environ, start_response)

