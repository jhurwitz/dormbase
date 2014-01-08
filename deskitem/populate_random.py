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
from deskitem.models import DeskItem, DeskItemLoan
from django.contrib.sites.models import Site
import random
import string

def rand_word(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))

def populate_random_desk_items():
    residents = Resident.on_site.all()[0:random.randint(5, 15)]
    s = Site.objects.get_current()
    items = []
    num_added = 0
    for i in range(30):
        item = DeskItem(
            at_dorm = s,
            name = rand_word(random.randint(4,10)),
        )
        if random.randint(0, 1) == 0:
            item.max_loan_duration = "%d days" % random.randint(1,5)
        item.save()
        num_added += 1
        items.append(item)
    print "Added %d desk items" % num_added
    num_added = 0
    for i in range(30):
        loan = DeskItemLoan(
            desk_item = random.choice(items),
            resident = random.choice(residents),
        )
        loan.save()
        num_added += 1
        if random.randint(0, 3) == 0:
            loan.end_loan()
    print "Added %d desk item loans" % num_added
