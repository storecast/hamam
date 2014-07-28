from ..base import BaseSessionStore
from .models import DjangoSession
from datetime import datetime


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