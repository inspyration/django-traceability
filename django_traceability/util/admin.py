"""
Admin interface manager.

TODO.
"""

from django.contrib import admin

from util.models import (
    Status,
    Country,
    StateCategory,
    State,
    Locale,
    TimeZone,
    UnitCategory,
    Unit,
    Currency,
)


class StatusAdmin(admin.ModelAdmin):
    """Customize Status admin interface"""

    list_display = ("label", "model")


class StateAdmin(admin.ModelAdmin):
    """Customize Country admin interface"""

    list_display = ("label", "country")


admin.site.register(Status, StatusAdmin)
admin.site.register(Country)
admin.site.register(StateCategory)
admin.site.register(State, StateAdmin)
admin.site.register(Locale)
admin.site.register(TimeZone)
admin.site.register(UnitCategory)
admin.site.register(Unit)
admin.site.register(Currency)
