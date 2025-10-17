from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserGroup
from .serializers_group import UserGroupSerializer


class UserGroupViewSet(viewsets.ModelViewSet):
    """用户分组视图集（仅管理员可操作）"""
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

