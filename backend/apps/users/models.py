from django.db import models
from django.contrib.auth.models import AbstractUser


class UserGroup(models.Model):
    """用户分组"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分组名称')
    description = models.TextField(blank=True, verbose_name='分组描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '用户分组'
        verbose_name_plural = verbose_name
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """扩展用户模型"""
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    department = models.CharField(max_length=100, blank=True, verbose_name='部门')
    position = models.CharField(max_length=100, blank=True, verbose_name='职位')
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='users', verbose_name='所属分组')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.username
    
    def get_group_members(self):
        """获取同组成员（包括自己）"""
        if self.group:
            return User.objects.filter(group=self.group, is_active=True)
        return User.objects.filter(id=self.id)  # 没有分组则只返回自己

