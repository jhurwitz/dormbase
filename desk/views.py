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
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import auth
from django.db.models import Q
from package.models import Package, PackageForm, CAN_MANAGE_PACKAGES_PERMISSION
from django.contrib.sites.models import Site
from residents.models import Resident
from deskitem.models import CAN_ADD_DESKITEMS_PERMISSION, CAN_LOAN_DESKITEMS_PERMISSION
from guestlist.models import GuestlistEntry
from common.lib import permission_required, make_boolean_checkmark_nofalse
from models import CAN_VIEW_DESK_SITE_PERMISSION
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview import helpers
from datetime import timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse

@permission_required(CAN_VIEW_DESK_SITE_PERMISSION)
def dashboard(request):
    payload = {}
    return render_to_response('desk/dashboard.html', payload, context_instance=RequestContext(request))

# permission_required() via urls.py
class PackageDatatableView(XEditableDatatableView):
    model = Package
    template_name = "desk/packages.html"
    datatable_options = {
        'columns': [
            ('Recipient', 'recipient', 'format_residents_name'),
            ('Notes', 'notes', helpers.make_xeditable),
            ('Delivered', 'delivered_at', 'format_delivered_at'),
            ('At desk?', 'retrieved_at', 'format_retrieved_at'),
            'tracking_number',
        ],
        'search_fields': ['recipient__user__first_name', 'recipient__user__last_name']
    }

    def format_residents_name(self, instance, *args, **kwargs):
        return instance.recipient.full_name

    def format_delivered_at(self, instance, *args, **kwargs):
        return instance.delivered_at.date()

    def format_retrieved_at(self, instance, *args, **kwargs):
        if instance.retrieved_at is None:
            return "&#10004; <small>[<a href='#' data-pk='%s' class='editable-click package-pickup'>click when picked up</a>]</small>" % instance.id
        else:
            return ""

    def get_queryset(self):
        # when someone picks up a package we don't want it to disappear
        # immediately, so show packages picked up within the past 5 minutes
        return Package.on_site.filter(Q(retrieved_at=None) | Q(retrieved_at__gte=timezone.now()-timedelta(minutes=5))) \
            .order_by('recipient__user__last_name')

    def get_context_data(self, **kwargs):
        context = super(PackageDatatableView, self).get_context_data(**kwargs)
        context['num_packages'] = Package.on_site.filter(retrieved_at=None).count()
        return context

@permission_required(CAN_MANAGE_PACKAGES_PERMISSION)
def package_pickup(request):
    pk = request.POST['pk']
    if pk is not None:
        Package.on_site.get(pk=pk).retrieved()
        return HttpResponse("ok")
    return HttpResponseBadRequest("bad")

@permission_required(CAN_MANAGE_PACKAGES_PERMISSION)
def package_scan(request):
    message = None
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            p = Package()
            p.at_dorm = Site.objects.get_current()
            p.recipient = form.cleaned_data['recipient']
            p.notes = form.cleaned_data['notes']
            p.tracking_number = form.cleaned_data['tracking_number']
            p.save()
            form = PackageForm()
            message = "Successfully scanned package for %s" % p.recipient.full_name
    else:
        form = PackageForm()

    payload = {'form': form, 'done_url': reverse('desk.views.packages')}
    if message is not None:
        payload['message'] = message
    return render_to_response('package/package_form.html', payload, context_instance=RequestContext(request))


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
