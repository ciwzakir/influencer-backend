from django.contrib import admin
from .models import FiscalYear,Month

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    # list_display = ('name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
