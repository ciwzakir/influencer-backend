from django.contrib import admin
from .models import Signatures, SuperInfo, Additional, AccountantsInfo, CounterSign, FinancialYear


@admin.register(Signatures)
class PrimarySettingsAdmin(admin.ModelAdmin):
    list_display = ('basic_info', 'with_effect_from')

@admin.register(SuperInfo)
class SuperInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'appointment')
    list_filter = ('name', 'rank', 'appointment')

@admin.register(Additional)
class AdditionalAdmin(admin.ModelAdmin):
    list_display = ('title','expense_incurred', 'cheque_series', 'unit_name')
    list_filter = ('expense_incurred', 'cheque_series', 'unit_name')

@admin.register(AccountantsInfo)
class AccountantsInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'appointment')
    list_filter = ('name', 'rank', 'appointment')

@admin.register(CounterSign)
class CounterInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'appointment')
    list_filter = ('name', 'rank', 'appointment')

admin.site.register(FinancialYear)
