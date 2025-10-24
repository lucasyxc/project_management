from rest_framework import serializers
from .models import Project, ProjectFile, ProjectStage
from apps.users.serializers import UserSerializer


class ProjectStageSimpleSerializer(serializers.ModelSerializer):
    """项目阶段简单序列化器（用于项目详情）"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = ProjectStage
        fields = ['id', 'name', 'description', 'order', 'deadline', 
                  'owner', 'owner_name', 'status', 'created_at']
    
    def to_representation(self, instance):
        """序列化时自动更新超期状态"""
        instance.update_status()
        return super().to_representation(instance)


class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器"""
    owner_detail = UserSerializer(source='owner', read_only=True)
    members_detail = UserSerializer(source='members', many=True, read_only=True)
    stages = ProjectStageSimpleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'priority', 'owner', 'owner_detail',
                  'members', 'members_detail', 'start_date', 'end_date', 'progress', 'budget',
                  'stages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'start_date', 'end_date', 'status', 'progress']
        extra_kwargs = {
            'owner': {'allow_null': True, 'required': False},
            'members': {'required': False},
        }


class ProjectListSerializer(serializers.ModelSerializer):
    """项目列表序列化器（简化版）"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    member_count = serializers.SerializerMethodField()
    current_stage = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'priority', 
                  'owner', 'owner_name', 'members', 'member_count', 'progress',
                  'start_date', 'end_date', 'current_stage', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_current_stage(self, obj):
        """获取当前进行中的步骤信息"""
        current_stage = obj.stages.filter(status='in_progress').order_by('order').first()
        if current_stage:
            return {
                'id': current_stage.id,
                'name': current_stage.name,
                'deadline': current_stage.deadline,
                'owner_name': current_stage.owner.username if current_stage.owner else None
            }
        return None


class ProjectFileSerializer(serializers.ModelSerializer):
    """项目文件序列化器"""
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = ProjectFile
        fields = '__all__'
        read_only_fields = ['uploaded_at']

