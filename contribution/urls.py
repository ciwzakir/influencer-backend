from django.contrib import admin
from . import views
from django.urls import path
from contribution.views import CollectionsViewsetWithFilterView
from rest_framework import routers

app_name = 'contribution'

router = routers.DefaultRouter()
router.register(r'collections', CollectionsViewsetWithFilterView, basename='collections')


urlpatterns = [
    # path('index', views.get_expense, name='index'),
   ] + router.urls


admin.site.site_header = "UTTORON ADMIN PANEL"
admin.site.index_title = "User Admin Dashboard"