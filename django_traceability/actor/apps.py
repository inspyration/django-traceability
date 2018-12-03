"""Application configuration file."""

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class ActorConfig(AppConfig):
    """
    Application configuration class.

    TODO
    """

    name = 'actor'
    verbose_name = _("Traceability tools - 02 - Actors")
