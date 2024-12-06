from django.contrib import admin
from .models import *


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id','user','source_name','amount']
    list_display_links = ['id','user',]
    list_filter = ['user','source_name','status']
    search_fields = ['user__username','status','source_name','amount']
    

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','user','category','amount']
    list_display_links = ['id','user',]
    list_filter = ['user','category','status']
    search_fields = ['user__username','status','category','amount']
    


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id','user','loan_name','status']
    list_display_links = ['id','user',]
    list_filter = ['user','loan_name','status']
    search_fields = ['user__username','status','loan_name']