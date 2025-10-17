from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProjectStage


@receiver(post_save, sender=ProjectStage)
def add_stage_owner_to_project_members(sender, instance, created, **kwargs):
    """阶段负责人自动添加到项目关联人"""
    if instance.owner:
        project = instance.project
        if instance.owner not in project.members.all():
            project.members.add(instance.owner)


@receiver([post_save, post_delete], sender=ProjectStage)
def update_project_status(sender, instance, **kwargs):
    """
    当阶段保存或删除时，自动更新项目状态、进度和日期
    规则：
    - 没有阶段 -> 项目未开始，进度0%
    - 有阶段但没有完成任何一个 -> 项目未开始，进度0%
    - 完成了至少一个阶段 -> 项目进行中，进度=(已完成数/总数)*100
    - 所有阶段都完成 -> 项目已完成，进度100%
    
    日期规则：
    - 开始日期 = 第一个完成的阶段的完成日期
    - 结束日期 = 最后一个（按order排序）完成的阶段的完成日期
    """
    project = instance.project
    stages = project.stages.all()
    
    if not stages.exists():
        # 没有阶段，项目未开始
        project.status = 'not_started'
        project.progress = 0
        project.start_date = None
        project.end_date = None
    else:
        # 统计各状态的阶段数量
        completed_stages = stages.filter(status='completed').order_by('order')
        completed_count = completed_stages.count()
        total_count = stages.count()
        
        # 计算进度
        project.progress = int((completed_count / total_count) * 100) if total_count > 0 else 0
        
        # 更新状态
        if completed_count == 0:
            # 没有完成任何阶段
            project.status = 'not_started'
            project.start_date = None
            project.end_date = None
        elif completed_count == total_count:
            # 所有阶段都完成了
            project.status = 'completed'
            # 开始日期 = 第一个完成的阶段
            first_completed = completed_stages.filter(completed_at__isnull=False).order_by('completed_at').first()
            project.start_date = first_completed.completed_at if first_completed else None
            # 结束日期 = 最后一个（按order）完成的阶段
            last_completed = completed_stages.filter(completed_at__isnull=False).last()
            project.end_date = last_completed.completed_at if last_completed else None
        else:
            # 至少完成了一个阶段
            project.status = 'in_progress'
            # 开始日期 = 第一个完成的阶段
            first_completed = completed_stages.filter(completed_at__isnull=False).order_by('completed_at').first()
            project.start_date = first_completed.completed_at if first_completed else None
            # 结束日期暂时为空（等所有阶段完成）
            project.end_date = None
    
    project.save()

