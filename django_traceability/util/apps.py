"""Application configuration file."""

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class UtilConfig(AppConfig):
    """
    Application configuration class.

    TODO
    """

    name = "util"
    verbose_name = _("Traceability tools - 01 - Utilities")
