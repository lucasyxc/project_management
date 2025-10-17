from django.db import models
from django.contrib.auth import get_user_model
from apps.projects.models import Project

User = get_user_model()


class Task(models.Model):
    """任务模型"""
    STATUS_CHOICES = [
        ('todo', '待办'),
        ('in_progress', '进行中'),
        ('review', '待审核'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='所属项目')
    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(blank=True, verbose_name='任务描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name='状态')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='assigned_tasks', verbose_name='负责人')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='创建者')
    
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='截止时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='预计工时')
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='实际工时')
    
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='subtasks', verbose_name='父任务')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TaskComment(models.Model):
    """任务评论"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name='所属任务')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '任务评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.task.title}'

