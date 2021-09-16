from rest_framework.viewsets import ModelViewSet

from ..models.event_code import EventCode, EventCodeSerializer
from ..auth.jwt_authentication import JwtAuthentication

class EventCodeView(ModelViewSet):
    """
    A view set that provides the standard actions for Event Code model
    """
    queryset = EventCode.objects.all()
    serializer_class = EventCodeSerializer
    authentication_classes = [JwtAuthentication]