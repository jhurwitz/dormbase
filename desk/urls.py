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

from django.conf.urls import patterns, url
from guestlist.models import CAN_VIEW_GUESTLISTS_PERMISSION
from common.lib import permission_required
import views

urlpatterns = patterns('desk.views',
    url(r'^$', views.dashboard),
    url(r'^packages/$', views.packages),
    url(r'^guestlists/$', permission_required(CAN_VIEW_GUESTLISTS_PERMISSION)(views.GuestlistDatatableView.as_view()), name='desk.views.guestlists'),
    url(r'^deskitems/$', views.deskitems),
)
