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
from package.models import Package
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required

import json

# TODO change to @permission_required once we've define a permission
@login_required
def package_get(request):
    if request.method != 'GET':
        raise Http404

    packages = []
    for p in Package.objects.all():
        packages.append({
                'recipient': p.recipient.full_name,
                'location': p.location,
                'id': p.id,
                })

    return HttpResponse(json.dumps(packages), mimetype='application/json')

# TODO change to @permission_required once we've define a permission
@login_required
def package_add(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            p = Package(recipient = cd['recipient'],
                        location = cd['location'],)
            p.save()

            jsonPackage = json.dumps({'recipient': p.recipient.full_name,
                                      'location': p.location,
                                      'id': p.id})

            return HttpResponse(jsonPackage, mimetype="application/json")

    raise Http404

# TODO change to @permission_required once we've define a permission
@login_required
def package_remove(request):
    if request.method == 'POST':
        p_id = request.POST['package_id']
        p = Package.objects.get(id = p_id)
        # TODO implement this
        pid = 'p' + str(p.id)
        jsonResponse = json.dumps({'id': pid})
        return HttpResponse(jsonResponse, mimetype="application/json")

    raise Http404
