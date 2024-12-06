# views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination




class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class IncomeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'source_name': ['exact', 'icontains'],
        'date_received': ['exact', 'gte', 'lte'],
        'status': ['exact'],
    }
    ordering_fields = ['amount', 'date_received', 'source_name']
    ordering = ['date_received']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the currently authenticated user
        serializer.save(user=self.request.user)




class ExpenseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'category': ['exact', 'icontains'],
        'due_date': ['exact', 'gte', 'lte'],
        'status': ['exact'],
    }
    ordering_fields = ['amount', 'due_date']
    ordering = ['amount']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the currently authenticated user
        serializer.save(user=self.request.user)
    


class LoanViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'loan_name': ['exact', 'icontains'],
        'status': ['exact'],
        'remaining_balance': ['gte', 'lte'],
    }
    ordering_fields = ['loan_name', 'principal_amount', 'remaining_balance']
    ordering = ['loan_name']  

    def get_queryset(self):
        print(self.request.user)
        return Loan.objects.filter(user=self.request.user)
    
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)