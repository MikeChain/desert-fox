from app import create_app
from config import envs

env = envs["dev"]
app = create_app(environment=env)
