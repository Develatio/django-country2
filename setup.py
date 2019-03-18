import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.md')).read()


setup(
    name='django-country2',
    version='0.0.1',
    url='https://github.com/Develatio/django-country2',
    author='Develatio Technologies S.L.',
    author_email='contacto@develat.io',
    description=('Provides Django middleware that detects '
                 'a country the request came from.'),
    long_description=README,
    packages=['django_country2'],
    include_package_data=True,
    scripts=[],
    extras_require={
        "pygeoip": ["pygeoip>=0.3.1"],
        "django-countries": ["django-countries>=5.3.3"],
    },
    zip_safe=False,
)
