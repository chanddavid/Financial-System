from rest_framework import serializers
from .models import *

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'source_name', 'amount', 'date_received', 'status', 'notes']

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("the amount cannot be negative")
        return value



class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'due_date', 'status', 'notes','date_received']



class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_name', 'principal_amount', 'interest_rate', 'tenure_months','remaining_balance', 'status', 'notes','date_received']
