from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import ProjectStage, Project
from .serializers_stage import ProjectStageSerializer, ProjectStageCreateSerializer


class ProjectStageViewSet(viewsets.ModelViewSet):
    """项目阶段视图集"""
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'status', 'owner']
    ordering_fields = ['order', 'deadline', 'created_at']
    ordering = ['order', 'id']
    
    def get_queryset(self):
        """
        普通用户只能看到自己相关项目的阶段
        管理员可以看到所有阶段
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # 管理员看所有
            return ProjectStage.objects.all()
        else:
            # 普通用户只看自己相关项目的阶段
            accessible_projects = Project.objects.filter(
                models.Q(owner=user) | models.Q(members=user)
            ).distinct()
            return ProjectStage.objects.filter(project__in=accessible_projects)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectStageCreateSerializer
        return ProjectStageSerializer

