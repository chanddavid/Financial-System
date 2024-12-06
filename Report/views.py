from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Count
from Management.models import Income, Expense, Loan
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from finance.logger import logger
from drf_yasg.utils import swagger_auto_schema




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FinancialSummary(request):
    try:
        filters = {'user': request.user}
        user = request.user
        logger.info(f" request of user {user}")
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')


        if start_date:
            filters['created_at__gte'] = start_date
        if end_date:
            filters['created_at__lte'] = end_date
        
        # Calculate total income, expenses, and active loans
        total_income = Income.objects.filter(**filters).aggregate(total_income=Sum('amount'))['total_income'] or 0
        total_expenses = Expense.objects.filter(**filters).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
        active_loans = Loan.objects.filter(**filters).filter(status='Active').aggregate(
            active_loans_count=Count('id'),
            active_loans_total=Sum('remaining_balance')
        )
        
        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'active_loans_count': active_loans['active_loans_count'] or 0,
            'active_loans_total': active_loans['active_loans_total'] or 0,
        })
    except Exception as e:
        logger.exception(stack_info=False, msg=f"Error={e.args}")
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)
        



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ReportVisualizationTrend(request):
    # Parse the query parameters for date filtering
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    filters = {'user': request.user}
    if start_date:
        filters['created_at__gte'] = start_date
    if end_date:
        filters['created_at__lte'] = end_date

    # Aggregate income and expenses by  
    income_data = Income.objects.filter(**filters).annotate(month=TruncMonth('created_at')) \
        .values('month').annotate(income_total=Sum('amount')).order_by('month')
    
    expenses_data = Expense.objects.filter(**filters).annotate(month=TruncMonth('created_at')) \
        .values('month').annotate(expenses_total=Sum('amount')).order_by('month')

    # Combine income and expenses data by month
    trend_data = []
    all_months = set(income_data.values_list('month', flat=True)) | set(expenses_data.values_list('month', flat=True))
    for month in sorted(all_months):
        income_for_month = next((item for item in income_data if item['month'] == month), None)
        expenses_for_month = next((item for item in expenses_data if item['month'] == month), None)
        trend_data.append({
            'month': month.strftime('%Y-%m'),
            'income': income_for_month['income_total'] if income_for_month else 0,
            'expenses': expenses_for_month['expenses_total'] if expenses_for_month else 0,
        })
    
    return Response({
        'income_vs_expenses_trend': trend_data
    })
