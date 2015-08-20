from django.conf.urls import url


urlpatterns = [
    url(r'^country/$', 'django_country.views.set_country', name='set_country'),
]
