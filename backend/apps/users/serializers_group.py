from rest_framework import serializers
from .models import UserGroup


class UserGroupSerializer(serializers.ModelSerializer):
    """用户分组序列化器"""
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserGroup
        fields = ['id', 'name', 'description', 'member_count', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True}
        }
    
    def get_member_count(self, obj):
        return obj.users.count()

