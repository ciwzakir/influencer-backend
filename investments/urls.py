from django.contrib import admin
from . import views
from django.urls import path
from rest_framework import routers

app_name = 'investments'

router = routers.DefaultRouter()
# router.register(r'mass-expenses', MasterViewsetView, basename='mass-expense')

urlpatterns = [
    # path('index', views.get_expense, name='index'),
   ] + router.urls


# admin.site.site_header = "Budget and Accounting "
# admin.site.index_title = "User Admin"