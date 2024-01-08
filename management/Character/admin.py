from django.contrib import admin

from Character.models import Character


class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ["map"]


admin.site.register(Character, CharacterAdmin)
