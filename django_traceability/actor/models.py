from functools import lru_cache

from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from util.mixins import SettingsMixin, CorporateMixin, StatusMixin, factory_image_mixin


class Actor(SettingsMixin, CorporateMixin, factory_image_mixin("logo", "Logo"), StatusMixin, PolymorphicModel):
    """Actor base class"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    @property
    @lru_cache(maxsize=1)
    def actor_type(self):
        """Provides a direct way to know the type of association"""
        return self.polymorphic_ctype.name.split()[-1].capitalize()

    #
    # Meta class
    #

    class Meta:  # pylint: disable=too-few-public-methods
        """Actor Meta class"""

        verbose_name = _("actor")
        verbose_name_plural = _("actors")
        ordering = ("label",)
