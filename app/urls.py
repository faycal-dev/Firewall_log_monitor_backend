from django.urls import path
from .views import filterLogs, AllLogs, filterIpLogs, filterDateLogs, MatriceDeFlux

urlpatterns = [
    path('severity/<str:query>/',filterLogs.as_view(), name='filterLogs' ),
    path('ip/<str:query>/',filterIpLogs.as_view(), name='filterIpLogs' ),
    path('date/<str:query>/',filterDateLogs.as_view(), name='filterIpLogs' ),
    path('MatriceDeFlux/',MatriceDeFlux.as_view(), name='MatriceDeFlux' ),
    path('severity/',AllLogs.as_view(), name='filterLogs' ),
]