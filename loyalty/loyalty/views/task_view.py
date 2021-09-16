from rest_framework.viewsets import ModelViewSet

from ..models.task import Task, TaskSerializer
from ..auth.jwt_authentication import JwtAuthentication

class TaskView(ModelViewSet):
    """
    A view set that provides the standard actions for Task model
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JwtAuthentication]