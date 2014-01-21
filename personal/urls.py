from django.conf.urls import patterns, url
import views

urlpatterns = patterns('personal.views',
    url(r'^$', views.dashboard),
    url(r'^profile/$', views.profile),
    url(r'^packages/$', views.packages),
    url(r'^guestlist/$', views.guestlist),
    url(r'^loans/$', views.loans),
)
