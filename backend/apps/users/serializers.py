from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserGroup

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'avatar', 'phone', 'department', 'position', 'group', 'group_name',
                  'is_active', 'is_staff', 'is_superuser', 'date_joined', 'created_at', 'updated_at']
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone', 'department', 'position', 'group']
        extra_kwargs = {
            'group': {'required': False, 'allow_null': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 
                  'phone', 'department', 'position', 'group']
        extra_kwargs = {
            'group': {'required': False, 'allow_null': True}
        }


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

