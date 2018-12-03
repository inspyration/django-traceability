"""TODO"""

from pathlib import Path
from uuid import uuid4

from django.db.models import (
    QuerySet,
    Model,
    DateTimeField,
    CharField,
    ForeignKey,
    PositiveSmallIntegerField,
    ImageField,
    Q,
    CASCADE, PROTECT)

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from django.db.models import (
    Manager,
)

from util.models import State, Country, Locale, TimeZone

from .fields import StatusField


class TimeFramedQuerySet(QuerySet):
    """QuerySet used by BaseMixin models"""

    def in_effect(self):
        """Allow to find an object that is currently valid"""
        current_date = now()
        return self.filter(
            Q(start__lte=current_date) & (
                Q(end__gte=current_date) | Q(end__isnull=True)
            )
        )

    def in_effect_at(self, date):
        """Allow to find an object that is valid at a specific date"""
        return self.filter(
            Q(start__lte=date) & (
                Q(end__gt=date) | Q(end__isnull=True)
            )
        )


class TimeFramedManager(Manager):
    """Manager for Models using the Time Framed Mixin"""

    def _get_queryset(self):
        """Link to the query set"""
        return TimeFramedQuerySet(self.model, using=self._db)

    def get_queryset(self):
        """Return the query set"""
        return self._get_queryset()

    @property
    def in_effect(self):
        """Get only active objects"""
        return self.get_queryset().in_effect()

    def in_effect_at(self, date):
        """Get only active objects"""
        return self.get_queryset().in_effect_at(date)


class TimeFramedMixin(Model):
    """Must be inherited by models that are valid only in a period of time"""

    #
    # Embedded QuerySet
    #

    class QuerySet(TimeFramedQuerySet):
        """Base QuerySet used by BaseMixin models that does not overwrite it"""

    # same default filters as BaseManager, with some other filters added
    time_framed_objects = TimeFramedManager()

    #
    # Define valid period
    #

    start = DateTimeField(
        verbose_name=_("start on"),
        blank=False,
        editable=True,  # TODO: Think about that
    )

    end = DateTimeField(
        verbose_name=_("end on"),
        null=True,
        blank=True,
        editable=True,  # TODO: Think about that
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """TimeFramedMixin Meta class"""

        abstract = True


class NaiveHierarchyManager(Manager):
    """Manager for Naive Hierarchy Mixin"""

    def __init__(self):
        super().__init__()
        self.root_filters = {}

    def get_roots(self, **kwargs):
        """Returns only first level objects"""
        self.root_filters = kwargs
        return self.get_queryset().filter(parent__isnull=True).filter(**kwargs)

    def get_children(self, node, *, use_root_filters=False):
        """Allow to get children propagating filters or not"""
        result = self.get_queryset().filter(parent=node)
        if use_root_filters and self.root_filters:
            result = result.filter(**self.root_filters)
        return result


class NaiveHierarchyMixin(Model):
    """Mixin that can be used in any model that have a hierarchy"""

    parent = ForeignKey(
        verbose_name=_("parent"),
        related_name="directory_set",
        help_text=_("Parent directory"),
        to="self",
        null=True,
        blank=True,
        on_delete=CASCADE,
    )

    tree = NaiveHierarchyManager()
    # objects = tree  # FIXME: Is this bug fix is relevant ?

    def get_children(self,):
        """Get children , whatever the filter used to find roots are"""
        return type(self).tree.get_children(self, use_root_filters=False).distinct()

    def get_filtered_children(self,):
        """Get children matching filters"""
        return type(self).tree.get_children(self, use_root_filters=True).distinct()

    def has_children(self):
        """Has children , whatever the filter used to find roots are"""
        return type(self).tree.get_children(self, use_root_filters=False).count() > 0

    def has_filtered_children(self):
        """Has children matching filters"""
        return type(self).tree.get_children(self, use_root_filters=True).count() > 0

    def get_descendants(self):
        """Get all descendant, whatever the filter used to find roots are"""
        result = set(self.get_children())
        for node in list(result):
            result.update(node.get_descendants())
        return result

    def get_filtered_descendants(self):
        """Get descendant while propagate filters"""
        result = set(self.get_filtered_children())
        for node in list(result):
            result.update(node.get_filtered_descendants())
        return result

    @classmethod
    def get_roots(cls, **kwargs):
        """Returns first level objetcs"""
        return cls.tree.get_roots(**kwargs)

    def _name_unique_model_path(self):
        """The logical model path to get the current object in a unique way"""
        if not self.parent:
            return self,
        else:
            return self.parent._name_unique_model_path() + (self,)  # pylint: disable=protected-access

    class Meta:  # pylint: disable=too-few-public-methods
        """NaiveHierarchyManager Meta class"""

        abstract = True


class StatusMixin(Model):
    """Must be inherited by models using a workflow based on status"""

    status = StatusField(
        verbose_name=_("status"),
        related_name="status_%(app_label)s_%(class)s_set",
        unique=False,
        blank=False,
        null=False,
        on_delete=PROTECT,
    )

    @classmethod
    def get_default_status(cls):
        """Automatically get the default status"""
        model = ".".join([
            cls._meta.app_label,
            cls._meta.model_name,
        ])
        return cls.objects.filter(model=model, is_default=True).first()

    class Meta:  # pylint: disable=too-few-public-methods
        """StatusMixin Meta class"""

        abstract = True


class LocalisationMixin(Model):
    """Add localisation information"""

    address1 = CharField(
        verbose_name=_("address 1"),
        help_text=_("first line of the address"),
        max_length=255,
        null=False,
        blank=False,
    )

    address2 = CharField(
        verbose_name=_("address 2"),
        help_text=_("second line of the address"),
        max_length=255,
        null=True,
        blank=True,
    )

    zip = CharField(
        verbose_name=_("zip"),
        help_text=_("Zip code"),
        max_length=16,
        null=False,
        blank=False,
    )

    city = CharField(
        verbose_name=_("city"),
        help_text=_("City"),
        max_length=255,
        null=False,
        blank=False,
    )

    state = ForeignKey(
        verbose_name=_("state"),
        related_name="%(app_label)s_%(class)s_set",
        help_text=_("State"),
        to=State,
        null=True,
        blank=True,
        on_delete=PROTECT,
    )

    country = ForeignKey(
        verbose_name=_("country"),
        related_name="%(app_label)s_%(class)s_set",
        help_text=_("Country"),
        to=Country,
        null=False,
        blank=False,
        on_delete=PROTECT,
    )

    @property
    def address(self):
        """Compile address"""
        result = [self.address1]
        if self.address2:
            result.append(self.address2)
        result.append(" ".join((self.zip, self.city, self.state.label)))
        result.append(self.country.label)
        return "\n".join(result)

    class Meta:  # pylint: disable=too-few-public-methods
        """LocalisationMixin Meta class"""

        abstract = True


class SettingsMixin(Model):
    """Allow to customize data (Dates and Language)"""

    locale = ForeignKey(
        verbose_name=_("locale"),
        related_name="%(app_label)s_%(class)s_set",
        help_text=_("Locale"),
        to=Locale,
        null=True,
        blank=True,
        on_delete=PROTECT,
    )

    timezone = ForeignKey(
        verbose_name=_("timezone"),
        related_name="%(app_label)s_%(class)s_set",
        help_text=_("Timezone"),
        to=TimeZone,
        null=False,
        blank=False,
        on_delete=PROTECT,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """SettingsMixin Meta class"""

        abstract = True


class WebMixin(Model):
    """Add Web information"""

    website = CharField(
        verbose_name=_("website"),
        help_text=_("Website URI"),
        max_length=64,
        null=True,
        blank=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """WebMixin Meta class"""

        abstract = True


class CorporateMixin(Model):
    """Describe a company"""

    tin = CharField(
        verbose_name=_("tin"),
        help_text=_("Tax intra. number"),
        max_length=16,
        null=False,
        blank=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """CorporateMixin Meta class"""

        abstract = True


def factory_image_mixin(field_name, field_label):
    class ImageMixin(Model):
        """Model can manage an avatar"""

        def compute_upload_path(self, filename):
            """Describe the image storage path"""
            today = now()
            return str(Path.joinpath(*list(map(Path, (self._meta.app_label,
                                                      self._meta.model_name,
                                                      field_name,
                                                      str(today.year),
                                                      str(today.month),
                                                      str(uuid4()) +
                                                      Path(filename).suffix)))))
        #
        # Meta class
        #

        class Meta:  # pylint: disable=too-few-public-methods
            """ImageMixin Meta class"""

            abstract = True

    setattr(ImageMixin, "{}_height".format(field_name), PositiveSmallIntegerField(
        verbose_name=_("logo height"),
        editable=False,
        null=True,
        blank=True,
    ))

    setattr(ImageMixin, "{}_width".format(field_name), PositiveSmallIntegerField(
        verbose_name=_("logo width"),
        editable=False,
        null=True,
        blank=True,
    ))

    setattr(ImageMixin, field_name, ImageField(
        verbose_name=_(field_label),
        max_length=64,
        upload_to=ImageMixin.compute_upload_path,
        height_field="{}_height".format(field_name),
        width_field="{}_width".format(field_name),
        null=True,
        blank=True,
    ))

    return ImageMixin
