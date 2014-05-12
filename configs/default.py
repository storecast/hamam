"""Here go the default config vars for staging, development and production."""

DEBUG = True

# dev specific configs
try: from .dev import *
except ImportError: pass
