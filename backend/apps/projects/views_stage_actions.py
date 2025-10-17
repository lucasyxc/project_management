from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectStage


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_stage_done(request, pk):
    """标记阶段为已完成"""
    try:
        stage = ProjectStage.objects.get(pk=pk)
        stage.mark_done()
        return Response({'message': '阶段已标记为完成', 'status': stage.status})
    except ProjectStage.DoesNotExist:
        return Response({'error': '阶段不存在'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_stage_redo(request, pk):
    """标记阶段为重做中"""
    try:
        stage = ProjectStage.objects.get(pk=pk)
        stage.mark_redo()
        return Response({'message': '阶段已改为重做中', 'status': stage.status})
    except ProjectStage.DoesNotExist:
        return Response({'error': '阶段不存在'}, status=status.HTTP_404_NOT_FOUND)
