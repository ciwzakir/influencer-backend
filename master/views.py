from django.shortcuts import render

# Create your views here.
from .models import Allotment, Category, Expenditure, Transaction,Refund

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from. serializers import ExpenditureSerializer, CodeWiseSerializer, SupplierWiseSerializer,ErrorSerializer,CategoryWiseSerializer, AllotmentSerializer, RefundSerializer,FinancialYearSerializer
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import F, Q
from datetime import datetime
from primary.models import FinancialYear
from rest_framework import (
    viewsets,
    filters,
    parsers,
    generics,
)
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CanDeleteDraftBill
from rest_framework.permissions import AllowAny 

def get_expense(request):
    expense_details = Expenditure.objects.all()
    context = {
        'expense_details':expense_details,
    }
    return render(request,'exp/index.html', context)

class FinancialYearViewSetView(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer

class MasterViewsetView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = ExpenditureSerializer
    ordering_fields = ['expenditure_code__is_general',]
    # filterset_fields = {'updated_at': ['gte', 'lte'],}

class ExpenseViewsetWithFilterView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.filter(
        is_published=True, 
    )
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = ExpenditureSerializer
    ordering_fields = ['expenditure_code__is_general',]
    ordering = ['-expenditure_code__is_general','expenditure_code__seven_digit_code' ]

class ChequeListFiltersView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.filter(
        is_published=True, 
        is_cheque=True, 
    )
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = ExpenditureSerializer
    ordering_fields = ['item_supplier__name',]
    ordering = ['item_supplier__name',]

class CashListFiltersView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.filter(
        is_published=True, 
        is_cheque=False, 
    )
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = ExpenditureSerializer
    ordering_fields = ['item_supplier__name',]

class DraftBillListFiltersViews(viewsets.ModelViewSet):
    queryset = Expenditure.objects.filter(
        is_published=False,  
        bills_status__in=[ 'AWAITING', 'PENDING']  # Explicit list of allowed statuses
    )
    serializer_class = ExpenditureSerializer
    permission_classes = [AllowAny]

class SentBackListFiltersViews(viewsets.ModelViewSet):
    queryset = Expenditure.objects.filter( 
       bills_status = 'SENT_BACK'
    )
    serializer_class = ExpenditureSerializer
    permission_classes = [AllowAny]      

class CodeWiseViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Expenditure.objects.all()
    serializer_class = CodeWiseSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields =  {
        'updated_at': ['gte', 'lte'],
        } 
     
        

class AllotmentViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Allotment.objects.all()
    serializer_class = AllotmentSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields = {'alloted_on': ['gte', 'lte'],}

class RefundViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields = {'refund_on': ['gte', 'lte'],}

class SupplierViewSetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Expenditure.objects.all()
    serializer_class = SupplierWiseSerializer

class CatgoryViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryWiseSerializer

class CatgoryViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryWiseSerializer

class ErrorViewsetView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    serializer_class = ErrorSerializer


    