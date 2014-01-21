from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.sites.models import Site
from residents.models import Resident
from django.http import Http404
from common.lib import resident_required

@login_required
def dashboard(request):
    try:
        resident = request.user.resident
    except Resident.DoesNotExist:
        return render_to_response('personal/non_resident.html', context_instance=RequestContext(request))

    payload = {'resident': request.user.resident}
    return render_to_response('personal/dashboard.html', payload, context_instance=RequestContext(request))

@resident_required()
def profile(request):
    payload = {'resident': request.user.resident}
    return render_to_response('personal/profile.html', payload, context_instance=RequestContext(request))

@resident_required()
def packages(request):
    return render_to_response('personal/packages.html', context_instance=RequestContext(request))

@resident_required()
def guestlist(request):
    return render_to_response('personal/guestlist.html', context_instance=RequestContext(request))

@resident_required()
def loans(request):
    return render_to_response('personal/loans.html', context_instance=RequestContext(request))
