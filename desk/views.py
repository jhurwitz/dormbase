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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.contrib import auth
from package.models import CAN_MANAGE_PACKAGES_PERMISSION
from residents.models import Resident
from guestlist.models import GuestlistEntry, CAN_VIEW_GUESTLISTS_PERMISSION
from deskitem.models import CAN_ADD_DESKITEMS_PERMISSION, CAN_LOAN_DESKITEMS_PERMISSION
from common.lib import permission_required
from models import CAN_VIEW_DESK_SITE_PERMISSION

@permission_required(CAN_VIEW_DESK_SITE_PERMISSION)
def dashboard(request):
    payload = {}
    return render_to_response('desk/dashboard.html', payload, context_instance=RequestContext(request))

@permission_required(CAN_MANAGE_PACKAGES_PERMISSION)
def packages(request):
    payload = {}
    return render_to_response('desk/packages.html', payload, context_instance=RequestContext(request))

@permission_required(CAN_VIEW_GUESTLISTS_PERMISSION)
def guestlists(request):
    payload = {}
    return render_to_response('desk/guestlists.html', payload, context_instance=RequestContext(request))

@permission_required([CAN_ADD_DESKITEMS_PERMISSION, CAN_LOAN_DESKITEMS_PERMISSION])
def deskitems(request):
    payload = {}
    return render_to_response('desk/deskitems.html', payload, context_instance=RequestContext(request))
