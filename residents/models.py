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
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from common.lib import ValidateOnSaveMixin

class Resident(ValidateOnSaveMixin, models.Model):
    STUDENT     = 'STU'
    HOUSEMASTER = 'HM'
    GRT         = 'GRT'
    AD          = 'AD'
    ROLE_CHOICES = (
        (STUDENT,     'Student'),
        (HOUSEMASTER, 'Housemaster'),
        (GRT,         'Graduate Resident Tutor'),
        (AD,          'Area Director'),
    )

    if settings.IS_UNDERGRAD_DORM:
        FRESHMAN    = 'FR'
        SOPHOMORE   = 'SO'
        JUNIOR      = 'JR'
        SENIOR      = 'SR'
        SUPERSENIOR = 'SS'
        YEAR_CHOICES = (
            (FRESHMAN,    'Freshman'),
            (SOPHOMORE,   'Sophomore'),
            (JUNIOR,      'Junior'),
            (SENIOR,      'Senior'),
            (SUPERSENIOR, 'Super-senior'),
        )
    else:
        GRAD1       = 'G1'
        GRAD2       = 'G2'
        GRAD3       = 'G3'
        GRAD4       = 'G4'
        GRAD5       = 'G5'
        GRAD6       = 'G6'
        GRAD7       = 'G7'
        YEAR_CHOICES = (
            (GRAD1, 'G1'),
            (GRAD2, 'G2'),
            (GRAD3, 'G3'),
            (GRAD4, 'G4'),
            (GRAD5, 'G5'),
            (GRAD6, 'G6'),
            (GRAD7, 'G7'),
        )

    user = models.OneToOneField(User, primary_key=True)
    dorm = models.ForeignKey(Site)
    room = models.CharField(max_length=10, validators=[validate_slug])
    # blank=False requires us to give a default
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, blank=False, default=STUDENT)
    # year is blank iff non-student (enforced by clean method)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, blank=True)

    objects = models.Manager()
    on_site = CurrentSiteManager('dorm')

    def clean(self):
        if self.role == Resident.STUDENT and self.year == "":
            raise ValidationError('Students must have a year')
        if self.role != Resident.STUDENT and self.year != "":
            raise ValidationError('Non-students cannot have a year')

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def __unicode__(self):
        return self.username
