from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Project, ProjectFile
from .serializers import (
    ProjectSerializer, ProjectListSerializer, ProjectFileSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """项目视图集"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'start_date', 'end_date', 'progress']
    
    def get_queryset(self):
        """
        普通用户只能看到自己相关的项目
        管理员可以看到所有项目
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # 管理员看所有
            return Project.objects.all()
        else:
            # 普通用户只看：自己是负责人或成员的项目
            return Project.objects.filter(
                models.Q(owner=user) | models.Q(members=user)
            ).distinct()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        # 创建项目，自动添加创建者为关联人
        project = serializer.save()
        if project.owner:
            project.members.add(project.owner)


class ProjectFileViewSet(viewsets.ModelViewSet):
    """项目文件视图集"""
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

