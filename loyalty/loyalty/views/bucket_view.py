from rest_framework.viewsets import ModelViewSet

from ..models.bucket import Bucket, BucketSerializer
from ..auth.jwt_authentication import JwtAuthentication

class BucketView(ModelViewSet):
    """
    A view set that provides the standard actions for Bucket model
    """
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    authentication_classes = [JwtAuthentication]
