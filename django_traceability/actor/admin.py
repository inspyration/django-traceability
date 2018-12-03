"""
Admin interface manager.

TODO.
"""

from django.contrib import admin

from actor.models import (
    Actor,
)


admin.site.register(Actor)
