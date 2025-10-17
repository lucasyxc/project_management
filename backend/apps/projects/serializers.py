from rest_framework import serializers
from .models import Project, ProjectFile
from apps.users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器"""
    owner_detail = UserSerializer(source='owner', read_only=True)
    members_detail = UserSerializer(source='members', many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """项目列表序列化器（简化版）"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'priority', 
                  'owner', 'owner_name', 'member_count', 'progress',
                  'start_date', 'end_date', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()


class ProjectFileSerializer(serializers.ModelSerializer):
    """项目文件序列化器"""
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = ProjectFile
        fields = '__all__'
        read_only_fields = ['uploaded_at']

