
from django.shortcuts import render
from .models import MonthlyContributionInfo, CollectionsInfo
from rest_framework.permissions import IsAuthenticated
from. serializers import CollectionsSerializer
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import F, Q
from datetime import datetime
from rest_framework import (
    viewsets,
    filters,
    parsers,
    generics,
)
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CanDeleteContributions
from rest_framework.permissions import AllowAny 


# class CollectionsViewsetWithFilterView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = CollectionsInfo.objects.all() 
    
#     # queryset = CollectionsInfo.objects.filter(
#     #     current_payment_status = "paid", 
#     # )
#     filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
#     serializer_class = CollectionsSerializer
#     ordering_fields = ['received_from',]
#     ordering = ['received_from']


class CollectionsViewsetWithFilterView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionsSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ['received_from',]
    ordering = ['received_from']

    def get_queryset(self):
        """
        Filter the queryset to only include collections for the logged-in user
        and only include records where payment status is 'paid'.
        """
        # Get the logged-in user
        user = self.request.user

        # Return the filtered queryset for the logged-in user and paid status
        return CollectionsInfo.objects.filter(
            received_from=user,
            # current_payment_status="paid"
        )
    
