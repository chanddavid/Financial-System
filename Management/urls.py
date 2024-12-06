from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *


app_name="management"


router = DefaultRouter()
router.register('incomes', IncomeViewSet, basename='income')
router.register('expenses', ExpenseViewSet, basename='expense')
router.register('loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
]
