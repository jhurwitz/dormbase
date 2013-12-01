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
