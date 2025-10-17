from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserGroup

User = get_user_model()


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'member_count', 'created_at']
    search_fields = ['name']
    
    def member_count(self, obj):
        return obj.users.count()
    member_count.short_description = '成员数'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'group', 'department', 'position', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'group', 'department']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('avatar', 'phone', 'department', 'position', 'group')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('额外信息', {'fields': ('email', 'phone', 'department', 'position', 'group')}),
    )
    
    def get_queryset(self, request):
        """管理员在后台可以看到所有用户"""
        return User.objects.all()

