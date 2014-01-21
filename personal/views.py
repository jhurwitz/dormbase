from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from residents.models import Resident
from django.http import Http404

@login_required
def dashboard(request):
    return render_to_response('personal/dashboard.html', context_instance=RequestContext(request))

@login_required
def profile(request):
    return render_to_response('personal/profile.html', context_instance=RequestContext(request))

@login_required
def packages(request):
    return render_to_response('personal/packages.html', context_instance=RequestContext(request))

@login_required
def guestlist(request):
    return render_to_response('personal/guestlist.html', context_instance=RequestContext(request))

@login_required
def loans(request):
    return render_to_response('personal/loans.html', context_instance=RequestContext(request))
