from django.contrib import admin
from .models import Allotment,Refund,Consumerunit, Category, Expenditure, Procurementprovider, Transaction



# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['seven_digit_code', 'heading', 'voucher_head','total_alloted_amounts','total_refund_amounts','progress_of_allotments','progress_of_expenses', 'current_balance']
    list_filter = ['seven_digit_code']
    prepopulated_fields = {'slug': ('name',)}

def save_related(self,request, obj, form, change):
        super(CategoryAdmin,self).save_related(request, obj, form, change)

@admin.register(Consumerunit)
class ConsumerunitAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent_office']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Procurementprovider)
class ProcurementproviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'address', 'tin_no', 'vat_no','is_registered','reg_date']
    list_filter = ['name', 'is_registered']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
    list_display = ['allotment_code', 'alloted_unit', 'title', 'slug', 'alloted_on','alloted_auth','alloted_amount']
    list_filter = ['allotment_code', 'alloted_unit', 'alloted_on']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['refund_code', 'refund_unit', 'title', 'slug', 'refund_on','refund_auth','refund_amount','approved']
    list_filter = ['refund_code', 'refund_unit','refund_on']
    prepopulated_fields = {'slug': ('title',)}

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):

    inlines =[
        TransactionInline,
    ]
    readonly_fields = ('total_allotments_codewise','total_expense_codewise','total_exp','total_tds','total_vds','total_paid')
    list_display = ['expenditure_code','total_exp','item_supplier', 'is_cheque','created_by','updated_at','is_published']
    # list_filter = ['title', ('created_at', PastDateRangeFilter), ('updated_at', FutureDateRangeFilter)]
    prepopulated_fields = {'slug': ('title',)}

    def save_related(self, request, form, formsets, change):
            super().save_related(request, form, formsets, change)
            form.instance.save()

