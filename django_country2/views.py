# -*- coding: utf-8 -*-
from django import http
from django.utils.http import is_safe_url

from . import geo


def set_country(request):
    """
    Sets the chosen country in the session or cookie.

    If `next' query param is present, it redirects to a given url.
    """
    if request.method == 'POST':
        next = request.POST.get('next', request.GET.get('next'))
        if is_safe_url(url=next, host=request.get_host()):
            response = http.HttpResponseRedirect(next)
        else:
            response = http.HttpResponse()

        country_code = request.POST.get('country', '').upper()
        if country_code != geo.get_supported_country(country_code):
            return http.HttpResponseBadRequest()

        if hasattr(request, 'session'):
            request.session[geo.COUNTRY_SESSION_KEY] = country_code
        else:
            response.set_cookie(geo.COUNTRY_COOKIE_NAME,
                               country_code,
                               max_age=geo.COUNTRY_COOKIE_AGE,
                               path=geo.COUNTRY_COOKIE_PATH)
        return response
    else:
        return http.HttpResponseNotAllowed(['POST'])
