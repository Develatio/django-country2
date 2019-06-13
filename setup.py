import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.md')).read()


setup(
    name='django-country2',
    version='0.0.7',
    url='https://github.com/Develatio/django-country2',
    author='Develatio Technologies S.L.',
    author_email='contacto@develat.io',
    description=('Provides Django middleware that detects a country the request came from.'),
    long_description=README,
    long_description_content_type="text/markdown",
    packages=['django_country2'],
    include_package_data=True,
    scripts=[],
    install_requires=[
        "geoip2>=2.9.0",
        "django-countries>=5.3.3",
    ],
    zip_safe=False,
)
