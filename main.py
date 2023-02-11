import os

from app import create_app
from config import envs

env = envs[os.environ.get("ENV")]
app = create_app(environment=env)
