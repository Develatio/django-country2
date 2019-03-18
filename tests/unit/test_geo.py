# -*- coding: utf-8 -*-
from mock import Mock
import unittest

from django.http.request import HttpRequest

from django_country2 import geo


class TestGetCountryFromRequest(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.original_use_geoip = geo.USE_GEOIP
        self.original_geo = geo._geo

    def tearDown(self):
        geo.USE_GEOIP = self.original_use_geoip
        geo._geo = self.original_geo

    def set_country_in_session(self):
        self.request.session = { geo.COUNTRY_SESSION_KEY: 'jp' }

    def set_country_in_cookie(self):
        self.request.COOKIES = { geo.COUNTRY_COOKIE_NAME: 'au' }

    def set_country_in_http_header(self):
        geo.USE_LOCALE = True
        self.request.META['HTTP_ACCEPT_LANGUAGE'] = 'en-gb'

    def set_country_with_ip(self):
        geo.USE_GEOIP = True
        geo._geo = Mock()
        geo._geo.country_code_by_addr.return_value='ca'
        self.request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1'

    def test_use_session_as_primary_source(self):
        self.set_country_in_session()
        self.set_country_in_cookie()
        self.set_country_with_ip()
        self.set_country_in_http_header()
        self.assertEqual(geo.get_country_from_request(self.request), 'JP')

    def test_use_cookie_as_secondary_source(self):
        self.set_country_in_cookie()
        self.set_country_with_ip()
        self.set_country_in_http_header()
        self.assertEqual(geo.get_country_from_request(self.request), 'AU')

    def test_use_ip_as_tertiary_source(self):
        self.set_country_with_ip()
        self.set_country_in_http_header()
        self.assertEqual(geo.get_country_from_request(self.request), 'CA')

    def test_use_http_header_if_other_sources(self):
        self.set_country_in_http_header()
        self.assertEqual(geo.get_country_from_request(self.request), 'GB')

    def test_use_default_if_no_sources_can_detect(self):
        self.assertEqual(geo.get_country_from_request(self.request), 'US')

    def test_fall_back_to_default_if_country_not_supported(self):
        self.request.session = { geo.COUNTRY_SESSION_KEY: 'AE' }
        self.assertEqual(geo.get_country_from_request(self.request), 'US')
