from django.contrib import admin
from links.models import Link


def unset_update(modeladmin, request, queryset):
    queryset.update(is_updated=False)
unset_update.short_description = "Mark selected links as no updated"


def public_on(modeladmin, request, queryset):
    queryset.update(is_public=True)
public_on.short_description = "Mark selected links as public"


def public_off(modeladmin, request, queryset):
    queryset.update(is_public=False)
public_off.short_description = "Mark selected links as private"


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'url', 'created_at', 'is_update', 'is_public')
    list_filter = ['created_at']
    search_fields = ['title', 'url']
    actions = [unset_update, public_on, public_off]


admin.site.register(Link, LinkAdmin)
