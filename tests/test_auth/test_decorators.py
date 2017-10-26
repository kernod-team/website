from flask import url_for

from app.auth.decorators import \
    catalog_roles_required, catalog_roles_accepted
from tests.bases import DecoratorBaseTestCase


class TestCatalogRolesRequired(DecoratorBaseTestCase):
    def get_decorator_in_question(self):
        return catalog_roles_required('math', ['member', 'mod'])

    def test_not_logged_in(self):
        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_no_required_roles(self):
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_no_all_required_roles(self):
        self.test_user['roles'] = ['math_member']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_incorrect_catalog(self):
        self.test_user['roles'] = ['cs_member', 'cs_mod']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_all_required_roles(self):
        self.test_user['roles'] = ['math_member', 'math_mod']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('decorator_pass', resp.get_data(as_text=True))


class TestCatalogRolesAccepted(DecoratorBaseTestCase):
    def get_decorator_in_question(self):
        return catalog_roles_accepted('math', ['member', 'mod'])

    def test_not_logged_in(self):
        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_no_accepted_roles(self):
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_no_all_accepted_roles(self):
        self.test_user['roles'] = ['math_member']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('decorator_pass', resp.get_data(as_text=True))

    def test_incorrect_catalog(self):
        self.test_user['roles'] = ['cs_member', 'cs_mod']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 403)

    def test_all_accepted_roles(self):
        self.test_user['roles'] = ['math_member', 'math_mod']
        self._log_in_as(self.test_user)

        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('decorator_pass', resp.get_data(as_text=True))
