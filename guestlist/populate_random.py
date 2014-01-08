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

from residents.models import Resident
from guestlist.models import GuestlistEntry
from django.contrib.sites.models import Site
import random

def populate_random_guests():
    s = Site.objects.get_current()
    f = open('residents/test_names.txt')
    names = [n.strip().split() for n in f.readlines()]
    residents = Resident.on_site.all()[0:random.randint(5, 15)]
    num_added = 0
    for r in residents:
        for i in range(5):
            first, last = random.choice(names)
            name = "%s %s" % (first, last)
            MIT = (random.randint(0,3) == 0)
            username = last[0:8].lower() if MIT else ""
            g = GuestlistEntry(
                guest_of = r,
                for_dorm = s,
                name = name,
                is_mit_student = MIT,
                username = username,
            )
            num_added += 1
            g.save()
    print "Added %d guest list entries" % num_added
