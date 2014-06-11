import base64
from datetime import datetime
from flask import current_app
from .serializers import JSONSerializer
from .models import DjangoSession, db
from functools import partial


class BaseSessionStore(object):
    """Base class for session storage.
    Normally read-only mode. You can create the session only while testing.
    Children must implement `_get` and `_set` methods.
    """

    # this is required to create a Django-ish session entry
    # since the session creation is supposed to be used for testing only,
    # not a realy hash here
    _hash = 'hash'

    def __init__(self, backend, key, serializer=None):
        self.backend = backend
        self.key = key
        self.serializer = serializer or JSONSerializer

    def load(self):
        session_data = self._get(self.key)

        if session_data is not None:
            return self._decode(session_data)
        else:
            return {}

    def put(self, session_data):
        if not current_app.config.get('TESTING'):
            raise NotImplementedError("This method is for testing purposes only")
        if session_data is None:
            raise ValueError("Session data cannot be None")
        encoded_data = self._encode(session_data)
        self._set(self.key, encoded_data)

    def _get(self, key):
        raise NotImplementedError

    def _set(self, key, session_data):
        raise NotImplementedError

    def _encode(self, session_data):
        """Encodes the session data in Django way.

        :param session_data: data to encode
        :type session_data: any serializable
        :return: encoded data
        :rtype: str
        """
        session_data = self.serializer().dumps(session_data)
        return base64.b64encode(bytes('%s:%s' % (self._hash, session_data)))

    def _decode(self, session_data):
        """Decodes the Django session.

        :param session_data: data to decode
        :type session_data: str
        :return: decoded data
        :rtype: dict
        """
        # django uses its `force_bytes` util, that meant to do more than that
        # we can happily use builtin `bytes` here
        decoded_data = base64.b64decode(bytes(session_data))
        try:
            # could produce ValueError if there is no ':'
            hash, serialized = decoded_data.split(b':', 1)
            return self.serializer().loads(serialized)
        except Exception:
            # ValueError, SuspiciousOperation, unpickling exceptions. If any of
            # these happen, return an empty dictionary (i.e., empty session).
            return {}


class DbSessionStore(BaseSessionStore):
    """Database session storage."""

    def _get(self, key):
        session = self.backend.session.query(DjangoSession).get(key)
        if session:
            return session.session_data

    def _set(self, key, session_data):
        session = DjangoSession(key, session_data, datetime.now())
        self.backend.session.add(session)
        self.backend.session.commit()

DbSessionStore = partial(DbSessionStore, db)
