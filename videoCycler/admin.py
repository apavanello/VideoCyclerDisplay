from django.contrib import admin
from django.contrib.auth.models import Group, User

from videoCycler.models import DisplayItem
from unfold.admin import ModelAdmin

# remover os grupos e usuários padrão do admin
for model in (Group, User):
    if model in admin.site._registry:
        admin.site.unregister(model)


@admin.register(DisplayItem)
class CustomAdminClass(ModelAdmin):
    list_display = ('title', 'media_type', 'duration_in_seconds', 'order', 'mute')
    list_filter = ('media_type',)
    search_fields = ('title',)
