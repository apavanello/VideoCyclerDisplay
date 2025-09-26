from django.contrib import admin

from videoCycler.models import DisplayItem
from unfold.admin import ModelAdmin

# Register your models here.

@admin.register(DisplayItem)
class CustomAdminClass(ModelAdmin):
    list_display = ('title', 'media_type', 'duration_in_seconds')
    list_filter = ('media_type',)
    search_fields = ('title',)


