# Django Country 2

This is a new version of [django-country](https://github.com/color/django-country) for the new versions of Django. A Django middleware that adds current country information to request object. The current country can be set manually or can be detected automatically
based on IP address or locale information in the HTTP header.

## Getting Started

Install django-country package:
```
pip install django-country2
```


Add the middleware in django settings:
```
# settings.py

MIDDLEWARE = [
    ...
    'django_country2.middleware.CountryMiddleware',
]
```
If you use `SessionMiddleware`, it needs to appear before `CountryMiddleware` in the list.

Now your can access detected country as a attribute of `request` object:
```
request.COUNTRY_CODE # Country code is in ISO 3166-1 alpha-2 format. e.g. "US"
```


Add an endpoint to set country manually:
```
# urls.py

urlpatterns = patterns('',
  ...
  url(r'/', include((django_country2.urls')),
)
```
Now you can send POST request to `<host>/country/` with `country` data
to set country manually.


Access country in Django templates:
```
# settings.py
TEMPLATE_CONTEXT_PROCESSORS = (
  ...
  'django_country2.context_processors.country',
)

# index.html
<div country-code={{country_code}}>{{country_name}}</div>
```


## How is country detected?

The middleware detects country from the following sources in the given order:

1. HEADER_FORCE_COUNTRY. Name of the heading to force the country code
1. session, if country code is set in session.
1. cookie, if country code is set in cookie.
1. IP address, if `settings.USE_GEOIP` is `True` (default: `False`).
1. HTTP_ACCEPT_LANGUAGE HTTP header if `settings.USE_LOCALE` is `True` (default: `False`).

## Settings

### HEADER_FORCE_COUNTRY
Default: `None`

Name of the heading to force the country code

### HEADER_REVERSE_PROXY_COUNTRY
Default: `None`

Name of the header that forwards the detected country code. Useful for use with reverse proxies such as CloudFlare. Set
this to CF-IPCountry to use the country code detected by CloudFlare. Remember that by default the XX or T1 countries are
invalid and will be ignored unless they are added to the list of countries in `COUNTRIES`.

### COUNTRY_CODE
Default: `'US'`

Country code to use if no country is detected.

### COUNTRIES
Default: A tuple of all countries. This list is retrieved from [django-countries](https://github.com/SmileyChris/django-countries) library.

This list is a tuble of two-tuples in the format (country code, country name) - for example ('JP', 'Japan'). This specifies which countries are available for country selection.

### USE_GEOIP
Default: `False`

A boolean that specifieds if IP address should be used to detect country. If this flag is set to `True`, `GEOIP_DAT_PATH` settings has to be specified.

### GEOIP_DAT_PATH
A path to geoip database in .dat format. You can download this from [MaxMind](http://dev.maxmind.com/geoip/legacy/geolite/#Downloads).

### USE_LOCALE
Default: `False`

A boolean that specifieds if locale information in ACCEPT-LANGUAGE HTTP header should be used to detect country.

### COUNTRY_SESSION_KEY
Default: `'django_country2'`

Session key under which the active country for the current session is stored.

### COUNTRY_COOKIE_NAME
Default: `'country'`

Cookie name under which the active country for the current session is stored.

### COUNTRY_COOKIE_AGE
Default: `None` (expires at browser close)

The age of the country cookie, in seconds.

### COUNTRY_COOKIE_PATH
Default: `/`

The path set on the country cookie. This should either match the URL
path of your Django installation or be a parent of that path.

This is useful if you have multiple Django instances running under the
same hostname. They can use different cookie paths and each instance
will only see its own country cookie.

Be cautious when updating this setting on a production site. If you
update this setting to use a deeper path than it previously used,
existing user cookies that have the old path will not be updated. This
will result in site users being unable to switch the country as long as
these cookies persist. The only safe and reliable option to perform the
switch is to change the country cookie name permanently.
