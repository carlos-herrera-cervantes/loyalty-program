from rest_framework.viewsets import ModelViewSet

from ..models.organization import Organization, OrganizationSerializer
from ..auth.jwt_authentication import JwtAuthentication

class OrganizationView(ModelViewSet):
    """
    A view set that provides the standard actions for Organization model
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [JwtAuthentication]