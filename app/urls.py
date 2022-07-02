from django.urls import path
from .views import filterLogs, AllLogs, filterIpLogs, filterDateLogs, MatriceDeFlux, Stats, SavedMatrices, GetSavedMatrices,VerifyAnomaly

urlpatterns = [
    path('severity/<str:query>/',filterLogs.as_view(), name='filterLogs' ),
    path('ip/<str:query>/',filterIpLogs.as_view(), name='filterIpLogs' ),
    path('date/<str:query>/',filterDateLogs.as_view(), name='filterIpLogs' ),
    path('MatriceDeFlux/',MatriceDeFlux.as_view(), name='MatriceDeFlux' ),
    path('stats/',Stats.as_view(), name='stats' ),
    path('severity/',AllLogs.as_view(), name='filterLogs' ),
    path('saved_logs/',SavedMatrices.as_view(), name='SavedLogs' ),
    path('get_saved_logs/',GetSavedMatrices.as_view(), name='GetSavedLogs' ),
    path('verify_anomaly/',VerifyAnomaly.as_view(), name='VerifyAnomaly' ),
]