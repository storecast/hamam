from . import get_session_store
from ..app import app
from mock import MagicMock
import os
import re
import tempfile
import unittest


class SessionViewTestCase(unittest.TestCase):

    session_key = 'some id'
    session_data = {'foo': 'bar'}

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % app.config['DATABASE']
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            self.store = get_session_store()
            # self.store = get_session_store()
            # self.store.backend.create_all()
            db = self.store.args[0]
            db.create_all()

    def tearDown(self):
        with app.app_context():
            # the session keeps some objects that were used during the test run
            # even if the db changes, the session connection stays the same
            # here we make sure that the session will be recreated
            # using `self.store` here to ensure that we refresh the exact session
            # that is used for `SessionStore`
            session = self.store.args[0].session
            session.remove()
            # self.store.backend.session.remove()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_no_cookie_data(self):
        """Shared session view returns empty response
        if there is no cookies.
        """
        rv = self.client.get('/session/')
        self.assertEqual('{}', rv.data)

    def test_content_type(self):
        """Shared session view returns correct
        `Content-Type` header.
        """
        rv = self.client.get('/session/')
        self.assertEqual('application/json', rv.content_type)

    def test_session_id_in_db(self):
        """Shared session view returns correct session data."""
        self.create_session()
        with self.client as c:
            c.set_cookie('*', app.config['SESSION_COOKIE_NAME'], self.session_key)
            rv = c.get('/session/')
            self.assertEqual(self.session_data, self.store('').serializer().loads(rv.data))

    def test_session_id_not_in_db(self):
        """Shared session view returns empty response
        if the session not in the db.
        """
        with self.client as c:
            c.set_cookie('*', app.config['SESSION_COOKIE_NAME'], self.session_key)
            rv = c.get('/session/')
            self.assertEqual('{}', rv.data)

    def create_session(self):
        """Helper that puts the session in the database."""
        with app.app_context():
            self.store(self.session_key).put(self.session_data)

    def strip_line(self, line):
        """Helper that strips all the whitespaces from the given string.

        :param line: string to strip
        :type line: str or unicode
        :return: stripped string
        :rtype: str or unicode
        """
        return re.sub(r'\s+', '', line)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SessionViewTestCase))
    return suite
