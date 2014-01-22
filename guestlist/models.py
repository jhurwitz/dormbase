from django.db import models
from django.db.models import Q
from residents.models import Resident
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from common.lib import ValidateOnSaveMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from django.core.validators import validate_slug

class GuestlistEntry(ValidateOnSaveMixin, models.Model):
    """
    A GuestlistEntry represents a single guest of a single resident.
    """
    guest_of = models.ForeignKey(Resident)
    # need this separately from resident's dorm (for security purposes,
    # guestlist entries should be tied to a particular dorm)
    for_dorm = models.ForeignKey(Site)

    name = models.CharField(max_length=30)
    is_mit_student = models.BooleanField(verbose_name='MIT student?')
    # this is a string username and not a User ForeignKey because it might be
    # an MIT student who doesn't have a Dormbase account yet
    username = models.CharField(max_length=10, blank=True, validators=[validate_slug])

    # save this information in case of security audits (e.g., if we need to
    # query who had access to the dorm on a given day)
    starts_on = models.DateField(default=timezone.now().date)
    # this is the first day when they will *not* have access to the dorm
    expires_on = models.DateField(null=True, blank=True, default=None)
    # set expires_on instead of deleting rows, and then if the person is re-
    # added, add a new row at that time

    objects = models.Manager()
    on_site = CurrentSiteManager('for_dorm')

    def __unicode__(self):
        return "%s, %s" % (self.guest_of, self.name)

    def clean(self):
        if self.is_mit_student and self.username == "":
            raise ValidationError('Students must have a username')
        if not self.is_mit_student and self.username != "":
            raise ValidationError('Non-students cannot have a username')

    @property
    def is_active(self):
        return self.expires_on == None or self.expires_on > timezone.now().date()

    def remove(self):
        if not self.is_active:
            raise ValueError("This guestlist entry has already been removed")
        self.expires_on = timezone.now().date()
        self.save()

    @classmethod
    def get_active_entries_for_dorm(cls, dorm=None):
        """
        Return the list of people allowed to enter dorm. This is the set of
        GuestlistEntries for dorm that have not been removed. If dorm=None,
        this will use the currently running site.
        """
        if dorm == None:
            dorm = Site.objects.get_current()
        return cls.objects.filter(Q(for_dorm=dorm),
            Q(expires_on__isnull=True) | Q(expires_on__gt=timezone.now().date()))

    @classmethod
    def get_active_entries_for_resident(cls, resident, dorm=None):
        """
        Return resident's guestlist. This is the set of GuestlistEntries for
        resident at dorm that have not been removed. If dorm=None, this will
        use the currently running site.
        """
        if dorm == None:
            dorm = Site.objects.get_current()
        return cls.objects.filter(Q(guest_of=resident), Q(for_dorm=dorm),
            Q(expires_on__isnull=True) | Q(expires_on__gt=timezone.now().date()))

    @classmethod
    def remove_all_active_entries_for_resident_outside_dorm(cls, resident, dorm=None):
        """
        Find all active guestlist entries for resident in dorms that are *not*
        the one passed as a parameter, and then call remove on each of them.
        Call this method after a resident switches dorms to invalidate their
        previous guestlist entries.

        If dorm=None, it defaults to the resident's *current dorm* (different
        from other methods in this class).
        """
        if dorm == None:
            dorm = resident.dorm
        entries = cls.objects.filter(
            Q(guest_of=resident),
            Q(expires_on__isnull=True) | Q(expires_on__gt=timezone.now().date())
        ).exclude(for_dorm=dorm)
        for entry in entries:
            entry.remove()

    @classmethod
    def get_active_entries_for_guest(cls, user):
        """
        Return the dorms that user can enter. This is the set of active
        GuestlistEntries for any dorm where the entry's username ==
        user.username.
        """
        return cls.objects.filter(Q(username=user.username),
            Q(expires_on__isnull=True) | Q(expires_on__gt=timezone.now().date()))

class GuestlistEntryForm(forms.ModelForm):
    class Meta:
        model = GuestlistEntry
        fields = ['name', 'is_mit_student', 'username', 'starts_on', 'expires_on']
        error_messages = {
            'username': {
                'invalid': "Enter just the username (the part before @mit.edu)",
            },
        }

# if you change these, make sure to update the fixtures!
CAN_VIEW_GUESTLISTS_PERMISSION = "can_view_guestlists"
