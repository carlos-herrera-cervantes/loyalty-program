from rest_framework.routers import SimpleRouter
from django.urls import path

from .views.campaign_view import CampaignView
from .views.user_view import UserView
from .views.login_view import LoginView

router = SimpleRouter()
router.register(r'api/v1/users', UserView)
router.register(r'api/v1/campaigns', CampaignView)

urlpatterns = [
    path(r'api/v1/auth/sign-in', LoginView.as_view())
]

urlpatterns += router.urls
