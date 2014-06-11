from flask import current_app, g
from werkzeug.local import LocalProxy
from werkzeug.utils import import_string


def get_session_store():
    """Returns the session store from the app globals."""
    if not hasattr(g, '_session_store'):
        g._session_store = import_string(current_app.config['SESSION_STORAGE'])
    return g._session_store

SessionStore = LocalProxy(get_session_store)
