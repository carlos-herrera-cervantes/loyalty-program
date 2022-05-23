from rest_framework.viewsets import ModelViewSet

from ..models.campaign import Campaign, CampaignSerializer
from ..auth.jwt_authentication import JwtAuthentication


class CampaignView(ModelViewSet):
    """
    A view set that provides the standard actions for Campaign model
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    authentication_classes = [JwtAuthentication]
