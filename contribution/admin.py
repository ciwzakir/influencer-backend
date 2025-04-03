from django.contrib import admin
from .models import MonthlyContributionInfo,CollectionsInfo


@admin.register(MonthlyContributionInfo)
class ContributionMonthAdmin(admin.ModelAdmin):
    list_display = ('name','fiscal_year', 'contribution_month','contribution_amount')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CollectionsInfo)
class CollectionsInfoAdmin(admin.ModelAdmin):
    list_display = ('received_from','receivable_month','amount','payment_image','total_paid_by_user','deposit_to','current_payment_status')
    prepopulated_fields = {'slug': ('title',)}