from django.urls import path
from .views import test_api, health_check

urlpatterns = [
    path('test/', test_api, name='test-api'),
    path('health/', health_check, name='health-check'),
]

