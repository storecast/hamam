from ..base import BaseSessionStore
from .models import db, DjangoSession
from contextlib import contextmanager
from datetime import datetime
from functools import partial


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.create_scoped_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class DbSessionStore(BaseSessionStore):
    """Database session storage."""

    def _get(self, key):
        session_data = None
        with session_scope() as backend_session:
            session = backend_session.query(DjangoSession).get(key)
            if session:
                session_data = session.session_data
        return session_data

    def _set(self, key, session_data):
        session = DjangoSession(key, session_data, datetime.now())
        self.backend.session.add(session)
        self.backend.session.commit()


SessionStore = partial(DbSessionStore, db)
