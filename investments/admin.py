from django.contrib import admin
from .models import InvestmentSectors,InvestmentsInfo


admin.site.register(InvestmentSectors)

@admin.register(InvestmentsInfo)
class ContributionMonthAdmin(admin.ModelAdmin):
    list_display = ('title','invested_on','investments_codes', 'investments_funds','invested_amount')
    prepopulated_fields = {'slug': ('title',)}
