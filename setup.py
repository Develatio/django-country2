from setuptools import setup


setup(
    name='django-country',
    version='0.1.0',
    url='https://github.com/ColorGenomics/django-country',
    author='Color Genomics, Inc.',
    author_email='katsuya@getcolor.com',
    description=('Provides Django middleware that detects '
                 'a country the request came from.'),
    packages=['django_country'],
    include_package_data=True,
    scripts=[],
    extras_require={
        "pygeoip": ["pygeoip>=0.3.1"],
        "django-countries": ["django-countries>=3.3"],
    },
    zip_safe=False,
)
