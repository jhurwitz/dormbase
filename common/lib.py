from django.contrib.sites.models import Site
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

class ValidateOnSaveMixin(object):
    """
    We are going to use validators to enforce model invariants. Models that
    extend this mixin will check validators when saving, so we know the
    invariants always hold.

    Code from http://www.xormedia.com/django-model-validation-on-save/
    """

    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update, **kwargs)


def permission_required(perm):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled for the current site through django-guardian. If the user is
    logged out, redirect to the login page. If the user lacks the permission,
    return a 403 error.

    This code is based on django.contrib.auth.decorators.permission_required
    """

    def check_perms(user):
        if not user.is_authenticated():
            return False
        try:
            resident = user.resident
        except ObjectDoesNotExist:
            # use the superclass ObjectDoesNotExist to avoid a circular import error
            raise PermissionDenied
        site = Site.objects.get_current()
        if resident.has_perm_for_dorm(perm, site):
            return True
        raise PermissionDenied
    return user_passes_test(check_perms)

def resident_required(dorm=None):
    """
    Decorator for views that checks whether a user is a resident of the
    specified dorm. (If no dorm is specified, use the current site.) If the
    user is logged out, redirect to the login page. If the user lacks the
    permission, return a 403 error.
    """

    if dorm == None:
        dorm = Site.objects.get_current()
    def is_resident(user):
        if not user.is_authenticated():
            return False
        try:
            resident = user.resident
        except ObjectDoesNotExist:
            # use the superclass ObjectDoesNotExist to avoid a circular import error
            raise PermissionDenied
        if resident.dorm == dorm:
            return True
        raise PermissionDenied
    return user_passes_test(is_resident)
