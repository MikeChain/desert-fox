from app import create_app
from config import envs
import os

env = envs[os.environ.get("ENV")]
app = create_app(environment=env)
