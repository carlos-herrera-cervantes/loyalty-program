from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.renderers import JSONRenderer
from json import loads

from ..models.campaign import Campaign, CampaignSerializer
from ..auth.jwt_authentication import JwtAuthentication

class CampaignView(ModelViewSet):
    """
    A view set that provides the standard actions for Campaign model
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    authentication_classes = [JwtAuthentication]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            result = Campaign.objects.create(**request.data)
            json = JSONRenderer().render(self.serializer_class(result).data)

            return Response(loads(json), content_type='application/json')

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
