from rest_framework import serializers
from .models import ProjectStage
from apps.users.serializers import UserSerializer


class ProjectStageSerializer(serializers.ModelSerializer):
    """项目阶段序列化器"""
    owner_detail = UserSerializer(source='owner', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = ProjectStage
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def to_representation(self, instance):
        """序列化时自动更新超期状态"""
        instance.update_status()
        return super().to_representation(instance)


class ProjectStageCreateSerializer(serializers.ModelSerializer):
    """项目阶段创建序列化器"""
    
    class Meta:
        model = ProjectStage
        fields = ['project', 'name', 'description', 'order', 'deadline', 'owner', 'status']
        extra_kwargs = {
            'owner': {'required': False, 'allow_null': True},
            'deadline': {'required': False, 'allow_null': True},
            'description': {'required': False},
            'order': {'required': False},
            'status': {'required': False}
        }

