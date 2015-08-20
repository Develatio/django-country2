# -*- coding: utf-8 -*-
from . import geo


def country(request):
    """
    Context processor that provides current country.
    """
    return {
        'country_code': request.COUNTRY_CODE,
        'country_name': geo.SUPPORTED_COUNTRIES[request.COUNTRY_CODE],
    }
