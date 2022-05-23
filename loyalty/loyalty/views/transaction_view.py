from json import loads
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_201_CREATED,
)

from ..models.transaction import Transaction, TransactionSerializer
from ..models.campaign import Campaign
from ..auth.jwt_authentication import JwtAuthentication
from ..decorators.transaction_decorator import (
    validate_customer,
    validate_event_code,
    transform_payload,
)


class TransactionView(ModelViewSet):
    """
    A view set that provides the standard actions for Transaction model
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JwtAuthentication]

    @action(methods=['post'], detail=False)
    @validate_customer
    @validate_event_code
    @transform_payload
    def queue(self, request: Request) -> Response:
        serializer: TransactionSerializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

        campaign: Campaign = Campaign.objects.get(id=request.data['campaign'])

        request.data.pop('campaign')

        created: Transaction = Transaction.objects.create(**request.data, campaign=campaign)
        json = JSONRenderer().render(TransactionSerializer(created).data)

        return Response(loads(json), status=HTTP_201_CREATED)
