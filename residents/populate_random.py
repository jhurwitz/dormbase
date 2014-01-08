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

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from residents.models import Resident
from django.contrib.sites.models import Site
import random

def populate_random_residents():
    s = Site.objects.get_current()
    f = open('residents/test_names.txt')
    names = [n.strip().split() for n in f.readlines()]
    num_added = 0
    for first, last in names:
        username = last[0:8].lower()
        email = "%s@mit.edu" % username
        try:
            u = User(first_name=first, last_name=last, username=username, email=email)
            u.save()
            if random.randint(0, 6) == 0:
                role = random.choice([Resident.HOUSEMASTER, Resident.GRT, Resident.AD])
                year = ""
            else:
                role = Resident.STUDENT
                year = random.choice([Resident.FRESHMAN, Resident.SOPHOMORE, Resident.JUNIOR, Resident.SENIOR])
            r = Resident(
                user = u,
                dorm = s,
                room = random.randint(1, 100),
                role = role,
                year = year,
            )
            r.save()
            num_added += 1
        except IntegrityError:
            continue
    print "Added %d residents" % num_added
