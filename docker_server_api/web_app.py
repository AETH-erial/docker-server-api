"""
FastAPI WebApp
"""
from fastapi import FastAPI
from docker_server_api.version import __version__
from docker_server_api.routers import example


web_app = FastAPI(title='docker-server-api', version=__version__,
                  description='Management API for controlling my docker setup')
web_app.include_router(example.router)
