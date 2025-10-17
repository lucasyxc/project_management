from rest_framework import serializers
from .models import Task, TaskComment
from apps.users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """任务序列化器"""
    assignee_detail = UserSerializer(source='assignee', read_only=True)
    creator_detail = UserSerializer(source='creator', read_only=True)
    subtask_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def get_subtask_count(self, obj):
        return obj.subtasks.count()


class TaskListSerializer(serializers.ModelSerializer):
    """任务列表序列化器（简化版）"""
    assignee_name = serializers.CharField(source='assignee.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'project', 'project_name', 'title', 'status', 'priority',
                  'assignee', 'assignee_name', 'due_date', 'created_at', 'updated_at']


class TaskCommentSerializer(serializers.ModelSerializer):
    """任务评论序列化器"""
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

