# Dormbase -- open-source dormitory database system
# Copyright (C) 2012 Alex Chernyakhovsky <achernya@mit.edu>
#                    Drew Dennison       <dennison@mit.edu>
#                    Isaac Evans         <ine@mit.edu>
#                    Luke O'Malley       <omalley1@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url
import views

import autocomplete_light
autocomplete_light.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Home page
    url(r'^$', views.home, name='home'),

    # Profile/Personal
    (r'^accounts/profile/', include('personal.urls')),

    # Authentication
    url(r'^accounts/login/$', 'mitauth.auth.scripts_login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    # Directory
    (r'^directory/', include('residents.urls')),

    # Desk
    (r'^desk/', include('desk.urls')),

    # Packages
    (r'^package/', include('package.urls')),

    # Nextbus
    (r'^nextbus/', include('nextbus.urls')),

    # Menu
    (r'^menus/', include('menus.urls')),

    # Laundry
    (r'^laundry/', include('laundry.urls')),

    # Facilities
    (r'^facilities/', include('facilities.urls')),

    # Resources
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #         'document_root': settings.MEDIA_ROOT
    #         }),

    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{
    #         'document_root': settings.STATIC_ROOT,
    #         }),

    url(r'^admin/', include(admin.site.urls)),

    # TODO check if we can add permissions to this
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)
