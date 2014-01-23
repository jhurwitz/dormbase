from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import timezone
from residents.models import Resident
from django.contrib.sites.models import Site
from package.models import Package
from guestlist.models import GuestlistEntry, GuestlistEntryForm
from deskitem.models import DeskItem, DeskItemLoan
from django.http import Http404
from common.lib import resident_required, make_boolean_checkmark_nofalse
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from datatableview.views import DatatableView
from datatableview import helpers

@login_required
def dashboard(request):
    try:
        resident = request.user.resident
    except Resident.DoesNotExist:
        return render_to_response('personal/non_resident.html', context_instance=RequestContext(request))

    num_packages = packages = Package.objects.filter(recipient=resident, retrieved_at=None).count()
    size_guestlist = GuestlistEntry.get_active_entries_for_resident(resident).count()
    num_active_loans = DeskItemLoan.get_active_loans_for_resident(resident).count()
    payload = {
        'resident': request.user.resident,
        'num_packages': num_packages,
        'size_guestlist': size_guestlist,
        'num_active_loans': num_active_loans,
    }
    return render_to_response('personal/dashboard.html', payload, context_instance=RequestContext(request))

@resident_required()
def profile(request):
    payload = {'resident': request.user.resident}
    return render_to_response('personal/profile.html', payload, context_instance=RequestContext(request))

@resident_required()
def packages(request):
    resident = request.user.resident
    # intentionally objects and not on_site
    packages = Package.objects.filter(recipient=resident, retrieved_at=None).order_by('delivered_at')
    payload = {
        'packages': packages,
    }
    return render_to_response('personal/packages.html', payload, context_instance=RequestContext(request))

@resident_required()
def guestlist(request):
    resident = request.user.resident
    guestlist_entries = GuestlistEntry.get_active_entries_for_resident(resident).order_by('-expires_on', 'name')
    payload = {
        'guests': guestlist_entries,
        'today': timezone.now().date(),
    }
    return render_to_response('personal/guestlist.html', payload, context_instance=RequestContext(request))

@resident_required()
def guestlist_add(request):
    if request.method == 'POST':
        form = GuestlistEntryForm(request.POST)
        if form.is_valid():
            g = GuestlistEntry()
            g.guest_of = request.user.resident
            g.for_dorm = Site.objects.get_current()
            g.name = form.cleaned_data['name']
            g.is_mit_student = form.cleaned_data['is_mit_student']
            g.username = form.cleaned_data['username']
            g.starts_on = form.cleaned_data['starts_on']
            g.expires_on = form.cleaned_data['expires_on']
            g.save()
            return HttpResponseRedirect(reverse(guestlist))
    else:
        form = GuestlistEntryForm(initial = {'is_mit_student': True})

    payload = {'form': form, 'prev_url': reverse(guestlist)}
    return render_to_response('guestlist/guestlistentry_form.html', payload, context_instance=RequestContext(request))

class GuestlistEntryDeleteView(DeleteView):
    model = GuestlistEntry
    success_url = reverse_lazy(guestlist)

    def get_context_data(self, **kwargs):
        context = super(GuestlistEntryDeleteView, self).get_context_data(**kwargs)
        context['prev_url'] = reverse(guestlist)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        # call remove() instead of deleting
        self.object.remove()
        return HttpResponseRedirect(success_url)

# resident_required() via urls.py
class DeskItemDatatableView(DatatableView):
    model = DeskItem
    template_name = "personal/deskitems.html"
    datatable_options = {
        'columns': [
            'name',
            'description',
            'max_loan_duration',
            ('At desk', 'at_desk', make_boolean_checkmark_nofalse),
        ]
    }

    def get_queryset(self):
        return DeskItem.on_site.all()

    def get_context_data(self, **kwargs):
        context = super(DeskItemDatatableView, self).get_context_data(**kwargs)
        resident = self.request.user.resident
        active_loans = DeskItemLoan.get_active_loans_for_resident(resident).order_by('loaned_at')
        context['active_loans'] = active_loans
        return context
