# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import trans_real

from django_countries import countries


DEFAULT_COUNTRY_CODE = getattr(settings, 'COUNTRY_CODE', 'US').upper()
SUPPORTED_COUNTRIES = dict(getattr(settings, 'COUNTRIES', countries.countries))
COUNTRY_SESSION_KEY = getattr(settings, 'COUNTRY_SESSION_KEY', 'django_country2')
COUNTRY_COOKIE_NAME = getattr(settings, 'COUNTRY_COOKIE_NAME', 'country')
COUNTRY_COOKIE_AGE = getattr(settings, 'COUNTRY_COOKIE_AGE', None)
COUNTRY_COOKIE_PATH = getattr(settings, 'COUNTRY_COOKIE_PATH', '/')
HEADER_FORCE_COUNTRY = getattr(settings, 'HEADER_FORCE_COUNTRY', None)
USE_GEOIP = getattr(settings, 'USE_GEOIP', False)
USE_LOCALE = getattr(settings, 'USE_LOCALE', False)

# Default country must be supported.
assert DEFAULT_COUNTRY_CODE in SUPPORTED_COUNTRIES

# Format of Accept-Language header values. From RFC 2616, section 14.4 and 3.9
# and RFC 3066, section 2.1. If country code is present, it will look something
# like "en-US".
LANG_COUNTRY_DELIM = '-'

_geo = None
if USE_GEOIP:
    assert bool(settings.GEOIP_DAT_PATH)
    import pygeoip
    _geo = pygeoip.GeoIP(settings.GEOIP_DAT_PATH)

def get_country_from_request(request):
    """
    Analyzes the request to find which country the user wants
    the system to recognize. It checks the following sources
    in the given order:
    * HEADER FORCE country
    * session,
    * cookie,
    * HTTP_ACCEPT_LANGUAGE HTTP header, and
    * IP address if USE_GEOIP is True.

    It returns country code in ISO 3166-1 alpha-2 format.
    """
    if HEADER_FORCE_COUNTRY:
        country_code = request.META.get(HEADER_FORCE_COUNTRY, None)
        if country_code:
            return get_supported_country(country_code)        

    if hasattr(request, 'session'):
        country_code = request.session.get(COUNTRY_SESSION_KEY)
        if country_code:
            return get_supported_country(country_code)

    country_code = request.COOKIES.get(COUNTRY_COOKIE_NAME)
    if country_code:
        return get_supported_country(country_code)

    if USE_GEOIP:
        ip = _extract_ip_address(request.META)
        country_code = _geo.country_code_by_addr(ip)
        if country_code:
            return get_supported_country(country_code)

    if USE_LOCALE:
        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        for accept_lang, _ in trans_real.parse_accept_lang_header(accept):
            if LANG_COUNTRY_DELIM in accept_lang:
                country_code = accept_lang.split(LANG_COUNTRY_DELIM)[-1]
                if country_code:
                    return get_supported_country(country_code)

    return DEFAULT_COUNTRY_CODE


def get_supported_country(country_code):
    """
    Returns the country code that's listed in supported countries.
    If a given code is not supported, it returns default country.
    """
    country_code = country_code.upper()
    if country_code in SUPPORTED_COUNTRIES:
        return country_code
    return DEFAULT_COUNTRY_CODE


def _extract_ip_address(meta):
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = meta.get('REMOTE_ADDR')
    return ip
