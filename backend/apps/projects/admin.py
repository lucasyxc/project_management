from django.contrib import admin
from .models import Project, ProjectFile, ProjectStage


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 0
    fields = ['name', 'order', 'deadline', 'owner', 'status']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'priority', 'owner', 'progress', 'start_date', 'end_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    date_hierarchy = 'created_at'
    inlines = [ProjectStageInline]


@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'order', 'deadline', 'owner', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'project__name']
    ordering = ['project', 'order']
    actions = ['mark_as_done']
    
    def mark_as_done(self, request, queryset):
        """批量标记为已完成"""
        count = 0
        for stage in queryset:
            if stage.status != 'completed':
                stage.mark_done()
                count += 1
        self.message_user(request, f'已标记{count}个阶段为完成')
    mark_as_done.short_description = '标记为已完成'


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['name', 'project__name']

