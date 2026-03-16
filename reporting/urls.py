from django.urls import path

from reporting.views import ReportView

urlpatterns = [
    path('report/' , ReportView.as_view(), name='report'),
]