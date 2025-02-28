from django.contrib import admin
from .models import Coach

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name', 'description')