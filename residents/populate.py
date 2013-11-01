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

from django.contrib.auth.models import User
from residents.models import Resident, Group, GroupMember
import random
import robotic_mailman

def import_test_directory():
    f = open('residents/test_names.txt')
    MAX_ROOM = 350

    for line in f.readlines():
        line = line.strip('\n')
        if '(' in line:
            continue
        line = line.split(' ')
        firstname, lastname = line[0], line[-1]
        if len(firstname) < 3 or len(lastname) < 3:
            continue
   #     print 'Adding ' + firstname + ' ' + lastname
        username = lastname[0:8].lower()
        print username
        u = User(first_name = firstname, last_name = lastname, username = username)
        u.save()
        r = Resident(user = u,
                     room = random.randint(1, MAX_ROOM),
                     athena = username,
                     year = random.choice([2012, 2013, 2014, 2015]),
                     livesInDorm = True)
        r.save()

        print 'Residents COMPLETE'

def make_fake_groups():
    nerds = Resident.objects.all()[0:5]
    topnerd = Resident.objects.all()[0]
    g = Group(name = 'tech-chair',
              mailingListName = 'tech-chair',
              autoSync = True,
              owner = None,
              memacl = None)
    g.save()
    nn = GroupMember(member = topnerd, group = g, position = "Tech Chair", autoMembership = True)
    nn.save()

    g2 = Group(name = 'simmons-tech',
              mailingListName = 'simmons-tech',
              autoSync = True,
              owner = g,
              memacl = None)
    g2.save()
    for n in nerds:
        gm = GroupMember(member = n, group = g2, position = "Tech Committee Member", autoMembership = True)        
        gm.save()

    print 'two groups created'
