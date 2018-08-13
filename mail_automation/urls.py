from django.conf.urls import url, include
from django.contrib import admin
from outlooksearch import views

urlpatterns = [
    # Invoke the home view in the outlooksearch app by default
    url(r'^$', views.home, name='home'),
    # Defer any URLS to the /outlooksearch directory to the outlooksearch app
    url(r'^outlooksearch/', include('outlooksearch.urls', namespace='outlooksearch')),
    url(r'^admin/', admin.site.urls),
]
