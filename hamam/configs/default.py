"""Here go the default config vars for staging, development and production."""

DEBUG = True

SESSION_COOKIE_NAME = 'sessionid'
SESSION_STORAGE = 'session.session_stores.DbSessionStore'

# path prefix to serve the documents from
DOCUMENT_PATH_PREFIX = '/delivery'

REAKTOR_CONFIG = {
    'host': 'skins-staging-reaktor',
    'port': 8080,
    'path': '/api/1.50.32/rpc',
    'ssl': False,
    'user_agent': 'hreaktor',
    'connect_timeout': 20,
    'run_timeout': 40,
    'communication_error_class': 'reaktor.ReaktorIOError',
    'http_service': 'services.httplib.HttpLibHttpService',
}


# dev specific configs
try: from .dev import *
except ImportError: pass
