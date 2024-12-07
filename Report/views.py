from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Count
from Management.models import Income, Expense, Loan
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from finance.logger import logger

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
            filters['date_received__gte'] = start_date
        if end_date:
            filters['date_received__lte'] = end_date
        
        # total income, expenses, and active loans
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
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')


    filters = {'user': request.user}
    if start_date:
        filters['date_received__gte'] = start_date
    if end_date:
        filters['date_received__lte'] = end_date

    # aggregate income and expenses by  
    income_data = Income.objects.filter(**filters).annotate(month=TruncMonth('date_received')).values('month').annotate(income_total=Sum('amount')).order_by('month')

    expenses_data = Expense.objects.filter(**filters).annotate(month=TruncMonth('date_received')).values('month').annotate(expenses_total=Sum('amount')).order_by('month')

    # combine income and expenses data by month
    visual_data = []
    
    income_dict = {item['month']: item['income_total'] for item in income_data}
    expenses_dict = {item['month']: item['expenses_total'] for item in expenses_data}

    sorted_data = sorted(set(income_dict.keys()) | set(expenses_dict.keys()))

    visual_data = [
            {
                'month': month.strftime('%Y-%m'),
                'income': income_dict.get(month, 0),
                'expenses': expenses_dict.get(month, 0),
            }
            for month in sorted_data
        ]
    return Response({'visual_data':visual_data})
