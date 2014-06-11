from flask import g, current_app
from werkzeug.local import LocalProxy
from holon import Reaktor
from barrel import config as barrel


def get_reaktor():
    """Returns the reaktor instance from the app globals."""
    if not hasattr(g, '_reaktor'):
        g._reaktor = Reaktor(**current_app.config['REAKTOR_CONFIG'])
    return g._reaktor

reaktor = lambda: LocalProxy(get_reaktor)

barrel.configure(REAKTOR=reaktor)
