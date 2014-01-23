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
from deskitem.models import CAN_ADD_DESKITEMS_PERMISSION, CAN_LOAN_DESKITEMS_PERMISSION
from guestlist.models import GuestlistEntry
from common.lib import permission_required, make_boolean_checkmark_nofalse
from models import CAN_VIEW_DESK_SITE_PERMISSION
from datatableview.views import DatatableView
from datatableview import helpers

@permission_required(CAN_VIEW_DESK_SITE_PERMISSION)
def dashboard(request):
    payload = {}
    return render_to_response('desk/dashboard.html', payload, context_instance=RequestContext(request))

@permission_required(CAN_MANAGE_PACKAGES_PERMISSION)
def packages(request):
    payload = {}
    return render_to_response('desk/packages.html', payload, context_instance=RequestContext(request))

# permission_required() via urls.py
class GuestlistDatatableView(DatatableView):
    # TODO we may want to have deskworkers log every time a guest enters the dorm
    model = GuestlistEntry
    template_name = "desk/guestlists.html"
    datatable_options = {
        'columns': [
            'name',
            ('MIT student?', 'is_mit_student', make_boolean_checkmark_nofalse),
            ('Guest of', 'guest_of', 'format_residents_name'),
            'starts_on',
            'expires_on'
        ],
        'search_fields': ['guest_of__user__first_name', 'guest_of__user__last_name']
    }

    def format_residents_name(self, instance, *args, **kwargs):
        return instance.guest_of.full_name

    def get_queryset(self):
        return GuestlistEntry.get_active_entries_for_dorm().order_by('name')

@permission_required([CAN_ADD_DESKITEMS_PERMISSION, CAN_LOAN_DESKITEMS_PERMISSION])
def deskitems(request):
    payload = {}
    return render_to_response('desk/deskitems.html', payload, context_instance=RequestContext(request))
