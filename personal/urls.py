from django.conf.urls import patterns, url

urlpatterns = patterns('personal.views',
    url(r'^$', 'dashboard'),
    url(r'^profile/$', 'profile'),
    url(r'^packages/$', 'packages'),
    url(r'^guestlist/$', 'guestlist'),
    url(r'^loans/$', 'loans'),
)
