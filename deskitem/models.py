from django.db import models
from residents.models import Resident
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
import datetime
import timedelta

class DeskItem(models.Model):
    """
    This is a generic desk item. You can subclass it to add more specific,
    structured details about a particular type of item, like a movie or a
    boardgame.
    """
    at_dorm = models.ForeignKey(Site)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, blank=True)
    max_loan_duration = timedelta.fields.TimedeltaField(null=True, default=None)
    resident_set = models.ManyToManyField(Resident, through='DeskItemLoan', related_name='desk_items')

    objects = models.Manager()
    on_site = CurrentSiteManager('at_dorm')

    def __unicode__(self):
        return self.name

    @property
    def at_desk(self):
        return self.desk_item_loans.filter(returned_at=None).count() == 0

    def loan_to_resident(self, resident):
        if not self.at_desk:
            raise ValueError("This item is not at desk")
        DeskItemLoan.objects.create(desk_item=self, resident=resident)

class DeskItemLoan(models.Model):
    desk_item = models.ForeignKey(DeskItem, related_name='desk_item_loans')
    resident = models.ForeignKey(Resident, related_name='desk_item_loans')
    # save time information (maybe an item is damaged and we'll want to query
    # the last 3 people to have borrowed it)
    loaned_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, default=None)

    def __unicode__(self):
        return "%s, %s" % (resident, desk_item)

    @property
    def due_by(self):
        duration = self.desk_item.max_loan_duration
        if duration is None:
            return None
        return self.loaned_at + duration

    def end_loan(self):
        if self.returned_at is not None:
            raise ValueError("This loan has already ended")
        self.returned_at = datetime.datetime.now()
        self.save()

    @classmethod
    def get_active_loans_for_resident(cls, resident):
        return cls.objects.filter(resident=resident, returned_at=None)
