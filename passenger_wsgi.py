import os
import sys
from a2wsgi import WSGIMiddleware
from src.main import app


sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
    return WSGIMiddleware(app, environ, start_response)
