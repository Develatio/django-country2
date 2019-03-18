# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin

from . import geo


class CountryMiddleware(MiddlewareMixin):
    """
    This is a middleware that parses a request
    and decides which country the request came from.
    """

    def process_request(self, request):
        request.COUNTRY_CODE = geo.get_country_from_request(request)
