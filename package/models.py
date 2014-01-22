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
from django import forms
from residents.models import Resident
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class Package(models.Model):
    recipient = models.ForeignKey(Resident)
    # need this separately from recipient's dorm (what if I receive a package
    # at an old address/a previous dorm?)
    at_dorm = models.ForeignKey(Site)
    # notes to help the deskworker locate the package, e.g., "two boxes" or
    # "large tube" or "on the bottom shelf"
    notes = models.CharField(max_length=50, blank=True)
    delivered_at = models.DateTimeField(auto_now_add=True)
    retrieved_at = models.DateTimeField(editable=False, null=True, default=None)
    tracking_number = models.CharField(max_length=30, blank=True)

    objects = models.Manager()
    on_site = CurrentSiteManager('at_dorm')

    def __unicode__(self):
        return "%s, %s" % (self.recipient, self.delivered_at.date())

    @property
    def at_recipients_dorm(self):
        return self.at_dorm == self.recipient.dorm

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package

# if you change these, make sure to update the fixtures!
CAN_MANAGE_PACKAGES_PERMISSION = "can_manage_packages"
