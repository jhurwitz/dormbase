from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from residents.models import Resident
from django.http import Http404

@login_required
def profile(request):
    return render_to_response('personal/profile.html', context_instance = RequestContext(request))

@login_required
def profile_username(request, username):
    try:
        resident = Resident.objects.get(user__username=username)  #need to query DB and get fullname
    except:
        raise Http404
    payload = {'fullname': resident.full_name,
               'room': resident.room, 'email': resident.email,
               'year': resident.year }

    return render_to_response('personal/user.html', payload, context_instance = RequestContext(request))
