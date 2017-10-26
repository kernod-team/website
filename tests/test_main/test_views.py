from flask import url_for

from tests.test_bases import ViewBaseTestCase


class TestIndex(ViewBaseTestCase):
    def test_index_accessible(self):
        self._log_in_as(self.test_user)
        resp = self.client.get(url_for('main.index'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('hello, world', resp.get_data(as_text=True))
