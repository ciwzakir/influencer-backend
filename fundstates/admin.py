from django.contrib import admin
from .models import AccountsInfo


@admin.register(AccountsInfo)
class ContributionMonthAdmin(admin.ModelAdmin):
    list_display = ('account_name','bank_name', 'branch_name','current_balance')
    prepopulated_fields = {'slug': ('account_name',)}
