from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime


@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    """测试API接口"""
    return Response({
        'status': 'success',
        'message': '后端服务运行正常！',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """健康检查接口"""
    return Response({
        'status': 'healthy',
        'service': 'project-management-api'
    })

