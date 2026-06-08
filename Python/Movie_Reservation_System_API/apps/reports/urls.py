from django.urls import path
from .views import ReservationReportView, RevenueReportView, CapacityReportView

urlpatterns = [
    path('reservations/', ReservationReportView.as_view(), name='report-reservations'),
    path('revenue/', RevenueReportView.as_view(), name='report-revenue'),
    path('capacity/', CapacityReportView.as_view(), name='report-capacity'),
]