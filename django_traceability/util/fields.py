"""TODO"""

from django.db import models
from django.db.models import ForeignKey

from .models import Status


class StatusField(ForeignKey):
    """A ForeignKey that point to status table"""

    def __init__(self, to=None, *args, **kwargs):
        """Initialisation of a Status Field"""
        if to is None:
            to = Status
        super(StatusField, self).__init__(to, *args, **kwargs)

    def get_default(self):
        """Get the default status"""
        result = Status.objects.filter(model=self.status_related_model,
                                       is_default=True).first()
        return result and result.id or None

    def prepare_class(self, sender, **kwargs):  # pylint: disable=unused-argument
        """Mandatory method: Allow to update the field on the fly to adapt it to the model"""
        if not sender._meta.abstract:  # TODO: use _meta alternative

            model = ".".join([
                sender._meta.app_label,  # TODO: use _meta alternative
                sender._meta.model_name,  # TODO: use _meta alternative
            ])
            self.status_related_model = model  # TODO: Do it otherwise
            self.remote_field.limit_choices_to = {"model": model}

    def contribute_to_class(self, cls, name, virtual_only=False):
        """Mandatory method: Allow to connect the previous method to related events"""
        models.signals.class_prepared.connect(self.prepare_class, sender=cls)
        super(StatusField, self).contribute_to_class(cls, name, virtual_only)
