from django.contrib import admin
from . import views
from django.urls import path
from master.views import (
    FinancialYearViewSetView,
    DraftBillListFiltersViews, 
    CashListFiltersView, 
    ChequeListFiltersView,
    ExpenseViewsetWithFilterView,
    MasterViewsetView,
    CodeWiseViewSetView,
    SupplierViewSetView,
    ErrorViewsetView,
    AllotmentViewSetView,
    RefundViewSetView,
    SentBackListFiltersViews
)


from rest_framework import routers

app_name = 'master'

router = routers.DefaultRouter()
router.register(r'mass-expenses', MasterViewsetView, basename='mass-expense')
router.register(r'mass-expenses/<pk>', MasterViewsetView, basename='mass-exp')
router.register(r'expenses-filters', ExpenseViewsetWithFilterView, basename='expenses-filters')
router.register(r'expenses-cheques', ChequeListFiltersView, basename='expenses-cheques')
router.register(r'expenses-cash', CashListFiltersView, basename='expenses-cash')
router.register(r'draft-bill', DraftBillListFiltersViews, basename='draft-bill')
router.register(r'draft-bill/<pk>', DraftBillListFiltersViews, basename='draft')
router.register(r'sent-back', SentBackListFiltersViews, basename='sent-back-records')
router.register(r'codes', CodeWiseViewSetView, basename='codes')
router.register(r'category', CodeWiseViewSetView, basename='cat')
router.register(r'supplier', SupplierViewSetView, basename='supplier')
router.register(r'allotments', AllotmentViewSetView, basename='allotments')
router.register(r'refunds', RefundViewSetView, basename='refunds')
router.register(r'fiscal-year', FinancialYearViewSetView, basename='fiscal-year')
router.register(r'error', ErrorViewsetView, basename='error_message')



urlpatterns = [
    path('index', views.get_expense, name='index'),
   ] + router.urls


admin.site.site_header = "Budget and Accounting "
admin.site.index_title = "User Admin"