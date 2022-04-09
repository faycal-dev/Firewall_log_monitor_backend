from django.urls import path
from .views import filterLogs, AllLogs

urlpatterns = [
    path('severity/<str:query>/',filterLogs.as_view(), name='filterLogs' ),
    path('severity/',AllLogs.as_view(), name='filterLogs' ),
]