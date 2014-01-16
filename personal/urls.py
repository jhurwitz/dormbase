from django.conf.urls import patterns, url

urlpatterns = patterns('personal.views',
    url(r'^$', 'profile'),
)
