from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet
from .views_group import UserGroupViewSet

router = DefaultRouter()
router.register(r'groups', UserGroupViewSet, basename='user-group')
router.register(r'', UserViewSet)

urlpatterns = [
    # JWT认证
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户相关
    path('', include(router.urls)),
]

