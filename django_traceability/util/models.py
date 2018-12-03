"""Generic models that can be use for any application"""


# TODO: Add a comment model


from django.db.models import (
    Model,
    BooleanField,
    CharField,
    PositiveSmallIntegerField,
    ForeignKey,
    ManyToManyField,
    FloatField, CASCADE, PROTECT)

from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields


#
# Status
#


class Status(Model):
    """Model handling all status"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    # Field that indicate the model related to the status
    # > not required
    # > default True
    # > editable
    model = CharField(  # TODO: Utiliser la table des modèles à la place.
        verbose_name=_("model"),
        help_text=_("Model related to the status"),
        max_length=64,
    )

    is_default = BooleanField(
        verbose_name=_("Is default ?"),
        help_text=_("Is the status is the default one for the model ?"),
        default=False,
    )

    # def compute_name(self):
    #     """The logical model path to get the current object in a unique way"""
    #     return "__".join((self.model.replace(".", "_"), self.label))

    class Meta:  # pylint: disable=too-few-public-methods
        """Status Meta class"""

        verbose_name = _("status")
        verbose_name_plural = _("statuses")


#
# Localization
#


class Country(Model):
    """Country"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    alpha2 = CharField(
        verbose_name=_("alpha2"),
        help_text=_("Two letters code"),
        max_length=2,
        unique=True,
    )

    alpha3 = CharField(
        verbose_name=_("alpha3"),
        help_text=_("Three letters code"),
        max_length=3,
        unique=True,
        blank=False,
    )

    number = PositiveSmallIntegerField(
        verbose_name=_("number"),
        help_text=_("Three digits number code"),
        unique=True,
        blank=False,
    )

    name_fr = CharField(
        verbose_name=_("french name"),
        help_text=_("French common name of the country"),
        max_length=255,
        unique=True,
        blank=False,
    )

    name_en = CharField(
        verbose_name=_("english name"),
        help_text=_("English common name of the country"),
        max_length=255,
        unique=True,
        blank=False,
    )

    usage = CharField(
        verbose_name=_("usage name"),
        help_text=_("Usage name (localised)"),
        max_length=255,
        unique=True,
        blank=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Country Meta class"""

        verbose_name = _("country")
        verbose_name_plural = _("countries")


class StateCategory(Model):
    """State"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    plural = CharField(
        verbose_name=_("plural"),
        help_text=_("Plural label"),
        max_length=127,
        blank=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """StateCategory Meta class"""

        verbose_name = _("state category")
        verbose_name_plural = _("state categories")


class State(Model):
    """State"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    code = CharField(
        verbose_name=_("code"),
        help_text=_("Two letters code"),
        max_length=5,
        unique=True,
        blank=False,
    )

    country = ForeignKey(
        verbose_name=_("country"),
        help_text=_("Related country"),
        related_name="state_set",
        to=Country,
        blank=False,
        on_delete=CASCADE,
    )

    category = ForeignKey(
        verbose_name=_("category"),
        help_text=_("State, Province or District"),
        related_name="registry_%(class)s_set",
        to=StateCategory,
        blank=False,
        on_delete=PROTECT,
    )

    def _name_unique_model_path(self):
        """The logical model path to get the current object in a unique way"""
        return self.country, self

    class Meta:  # pylint: disable=too-few-public-methods
        """State Meta class"""

        verbose_name = _("state")
        verbose_name_plural = _("states")


#
# Settings
#


class Locale(Model):
    """
    Locale model.

    label contains language code such as fr-fr
    name contains locale name such as fr_FR
    """

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    # def compute_name(self):
    #     language, country = self.label.split("-")
    #     return "_".join((language, country.upper()))

    class Meta:  # pylint: disable=too-few-public-methods
        """Locale Meta class"""

        verbose_name = _("locale")
        verbose_name_plural = _("locales")


class TimeZone(Model):
    """TimeZone"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """TimeZone Meta class"""

        verbose_name = _("timezone")
        verbose_name_plural = _("timezones")


#
# Units management
#


class UnitCategory(Model):
    """Configuration parameter"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """UnitCategory Meta class"""

        verbose_name = _("unit category")
        verbose_name_plural = _("unit categories")


class Unit(Model):
    """Configuration parameter"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    category = ForeignKey(
        verbose_name=_("category"),
        related_name="unit_set",
        help_text=_("Category"),
        to=UnitCategory,
        on_delete=PROTECT,
    )

    plural = CharField(
        verbose_name=_("plural"),
        help_text=_("Plural"),
        max_length=31,
        blank=False,
    )

    symbol = CharField(
        verbose_name=_("symbol"),
        help_text=_("Symbol"),
        max_length=7,
        blank=False,
    )

    value = FloatField(
        verbose_name=_("value"),
        help_text=_("Value converted in SI Unit"),
        blank=False,
    )

    def _name_unique_model_path(self):
        return self.category, self

    class Meta:  # pylint: disable=too-few-public-methods
        """Unit Meta class"""

        verbose_name = _("unit")
        verbose_name_plural = _("units")


class Currency(Model):
    """Configuration parameter"""

    label = CharField(
        verbose_name=_("Label"),
        help_text=_("The way this object will be represented"),
        max_length=255,
        unique=False,
        blank=False,
    )

    plural = CharField(
        verbose_name=_("plural"),
        help_text=_("Plural"),
        max_length=31,
        blank=False,
    )

    symbol = CharField(
        verbose_name=_("symbol"),
        help_text=_("Symbol"),
        max_length=7,
        blank=False,
    )

    iso_code = CharField(
        verbose_name=_("iso code"),
        help_text=_("Iso 4217 code"),
        max_length=3,
        blank=False,
    )

    value = FloatField(
        verbose_name=_("value"),
        help_text=_("amount to 1 euros"),
        blank=True,
        null=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Currency Meta class"""

        verbose_name = _("currency")
        verbose_name_plural = _("currencies")
