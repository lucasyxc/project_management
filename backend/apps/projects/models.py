from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    """项目模型"""
    STATUS_CHOICES = [
        ('not_started', '未开始'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='项目名称')
    description = models.TextField(blank=True, verbose_name='项目描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='状态')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low', verbose_name='优先级')
    
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='owned_projects', verbose_name='项目负责人')
    members = models.ManyToManyField(User, related_name='projects', blank=True, verbose_name='项目成员')
    
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='结束日期')
    
    progress = models.IntegerField(default=0, verbose_name='进度(%)')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='预算')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    """项目阶段"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages', verbose_name='所属项目')
    name = models.CharField(max_length=100, verbose_name='阶段名称')
    description = models.TextField(blank=True, verbose_name='阶段描述')
    order = models.IntegerField(default=0, verbose_name='排序')
    
    # 截止日期（非必填）
    deadline = models.DateField(null=True, blank=True, verbose_name='截止日期')
    
    # 负责人
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='managed_stages', verbose_name='阶段负责人')
    
    # 状态
    STATUS_CHOICES = [
        ('in_progress', '进行中'),
        ('overdue', '已超期'),
        ('completed', '已完成'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name='状态')
    completed_at = models.DateField(null=True, blank=True, verbose_name='实际完成日期')
    
    def update_status(self):
        """更新状态：检查是否超期"""
        from datetime import date
        if self.status != 'completed' and self.deadline and date.today() > self.deadline:
            self.status = 'overdue'
            self.save()
    
    def mark_done(self):
        """标记为已完成"""
        from datetime import date
        self.status = 'completed'
        self.completed_at = date.today()
        self.save()
    
    def mark_redo(self):
        """标记为重做中"""
        self.status = 'in_progress'
        self.completed_at = None  # 清除完成日期
        self.save()
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '项目阶段'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']
    
    def __str__(self):
        return f'{self.project.name} - {self.name}'


class ProjectFile(models.Model):
    """项目文件"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files', verbose_name='所属项目')
    name = models.CharField(max_length=200, verbose_name='文件名')
    file = models.FileField(upload_to='project_files/', verbose_name='文件')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传者')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        verbose_name = '项目文件'
        verbose_name_plural = verbose_name
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.name

