from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectFileViewSet
from .views_stage import ProjectStageViewSet
from .views_stage_actions import mark_stage_done, mark_stage_redo

router = DefaultRouter()
router.register(r'stages', ProjectStageViewSet, basename='project-stage')
router.register(r'files', ProjectFileViewSet)
router.register(r'', ProjectViewSet)

urlpatterns = [
    path('stages/<int:pk>/done/', mark_stage_done, name='stage-done'),
    path('stages/<int:pk>/redo/', mark_stage_redo, name='stage-redo'),
    path('', include(router.urls)),
]

