from django.conf.urls import patterns, url
import views

urlpatterns = patterns('personal.views',
    url(r'^$', views.dashboard),
    url(r'^profile/$', views.profile),
    url(r'^packages/$', views.packages),
    url(r'^guestlist/$', views.guestlist),
    url(r'^guestlist/add/$', views.guestlist_add),
    url(r'^guestlist/remove/(?P<pk>\d+)/$', views.GuestlistEntryDeleteView.as_view(), name='personal.views.guestlistentry_delete'),
    url(r'^loans/$', views.loans),
)
