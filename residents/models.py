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

from django.db import models
from django.core.validators import validate_slug
from django.contrib.auth.models import User as AuthUser


class AbstractResident(models.Model):
    """
    Abstract class containing all non-dorm-specific user attributes.
    Maintains a 1-1 with the auth app user module.
    """
    user = models.ForeignKey(AuthUser, unique = True)
    room = models.CharField(max_length = 10, blank = False)
    athena  = models.CharField(max_length = 8, verbose_name = "athena id") # no "@mit.edu" suffix
    year = models.IntegerField()
    altemail = models.EmailField(verbose_name="non-MIT email", blank = True)
    url = models.CharField(max_length = 256, blank = True)
    about = models.TextField(blank = True)
    livesInDorm = models.BooleanField()

    def __unicode__(self):
        return self.athena

    def getFullName(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        abstract = True

class Resident(AbstractResident):
    """
    This class contians user attributes which are dorm-specific.
    """
    title = models.CharField(max_length = 50, blank = True)
    cell = models.CharField(max_length = 20, blank = True)
    hometown = models.CharField(max_length = 200, blank = True)

    @models.permalink
    def get_absolute_url(self):
        return ('dormbase.personal.views.profile_username', (),
                {'username': self.athena})
