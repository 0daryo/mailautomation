from django.conf.urls import url 
from outlooksearch import views 

app_name = 'outlooksearch'
urlpatterns = [ 
  # The home view ('/outlooksearch/') 
  url(r'^$', views.home, name='home'), 
  # Explicit home ('/outlooksearch/home/') 
  url(r'^home/$', views.home, name='home'), 
  # Redirect to get token ('/outlooksearch/gettoken/')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  # Mail view ('/outlooksearch/mail/')
  url(r'^mail/$', views.mail, name='mail'),
]