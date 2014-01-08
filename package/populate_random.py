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
from package.models import Package
from django.contrib.sites.models import Site
from django.utils import timezone
import random

def populate_random_packages():
    residents = Resident.on_site.all()[0:random.randint(5, 15)]
    s = Site.objects.get_current()
    num_added = 0
    for r in residents:
        for i in range(random.randint(0, 5)):
            p = Package(
                recipient = r,
                at_dorm = s,
            )
            if random.randint(0, 3) > 0:
                p.retrieved_at = timezone.now()
            p.save()
            num_added += 1
    print "Added %d packages" % num_added
