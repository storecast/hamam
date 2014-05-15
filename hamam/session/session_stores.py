import base64
from .serializers import JSONSerializer
from .models import DjangoSession


class BaseSessionStore(object):
    """Base class for session storage.
    Read-only mode for sessions.
    Children must implement `get` method.
    """

    def __init__(self, backend, key, serializer=None):
        self.backend = backend
        self.key = key
        self.serializer = serializer or JSONSerializer

    def load(self):
        session_data = self.get(self.key)

        if session_data is not None:
            return self._decode(session_data)
        else:
            return {}

    def get(self, key):
        raise NotImplemented

    def _decode(self, session_data):
        """Decodes the Django session.

        :param session_data: data to decode
        :type session_data: str
        :return: decoded data
        :rtype: dict
        """
        # django uses its `force_bytes` util, that meant to do more than that
        # we can happily use builtin `bytes` here
        encoded_data = base64.b64decode(bytes(session_data))
        try:
            # Could produce ValueError if there is no ':'
            hash, serialized = encoded_data.split(b':', 1)
            return self.serializer().loads(serialized)
        except Exception:
            # ValueError, SuspiciousOperation, unpickling exceptions. If any of
            # these happen, return an empty dictionary (i.e., empty session).
            return {}


class DbSessionStore(BaseSessionStore):
    """Database session storage."""

    def get(self, key):
        session = DjangoSession.query.get(key)
        if session:
            return session.session_data
