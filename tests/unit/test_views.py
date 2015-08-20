# -*- coding: utf-8 -*-
from mock import Mock
import unittest

from django.http.request import HttpRequest

from django_country import geo
from django_country.views import set_country


class TestSetCountry(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.get_host = Mock(return_value='localhost')

    def test_set_session_if_available(self):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST['country'] = 'JP'
        response = set_country(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.request.session[geo.COUNTRY_SESSION_KEY], 'JP')

    def test_set_cookie_if_session_is_unavailable(self):
        self.request.method = 'POST'
        self.request.POST['country'] = 'JP'
        response = set_country(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies[geo.COUNTRY_COOKIE_NAME].value, 'JP')

    def test_redirect_if_next_url_is_given(self):
        self.request.method = 'POST'
        self.request.GET['next'] = 'example.com'
        self.request.POST['country'] = 'JP'
        response = set_country(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'example.com')

    def test_return_400_if_unsupported_country_is_given(self):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST['country'] = 'HEAVEN'
        response = set_country(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(geo.COUNTRY_SESSION_KEY in self.request.session)

    def test_only_post_allowed(self):
        self.request.method = 'GET'
        response = set_country(self.request)
        self.assertEqual(response.status_code, 405)
