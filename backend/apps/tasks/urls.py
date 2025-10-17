from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskCommentViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet)
router.register(r'comments', TaskCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

