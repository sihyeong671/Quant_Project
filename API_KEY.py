from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

APIKEY = env('APIKEY')
USERAGENT = env('USERAGENT')
