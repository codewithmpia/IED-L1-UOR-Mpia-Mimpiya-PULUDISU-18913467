import os 
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "assets/templates"

STATIC_DIR = BASE_DIR / "assets/static"

# For development
DEV_KEY = "unzf9jsr3uk4^4meg5in62z9k#d^nadm42&2x%n$$8)d4nj=-s"


def get_env_vars(name, default):
  env = os.getenv(name)
  if env is None:
    if default is None:
      raise ValueError("Ne peut être vide.")
    return default
  return env