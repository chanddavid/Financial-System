from django.urls import path
from .views import *

app_name="report"


urlpatterns = [
    path('financial_summary/', FinancialSummary, name='financial_summary'),
    path('report_visualization_trend/', ReportVisualizationTrend, name='report_visualization_trend'),
]
