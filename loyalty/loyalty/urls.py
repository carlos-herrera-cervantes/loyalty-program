from rest_framework.routers import SimpleRouter
from django.urls import path

from .views.campaign_view import CampaignView
from .views.user_view import UserView
from .views.auth_view import AuthView

router = SimpleRouter()
router.register(r'api/v1/users', UserView)
router.register(r'api/v1/campaigns', CampaignView)

sign_in = AuthView.as_view({'post': 'sign_in'})
logout = AuthView.as_view({'post': 'logout'})

urlpatterns = [
    path(r'api/v1/auth/sign-in', sign_in),
    path(r'api/v1/auth/logout', logout)
]

urlpatterns += router.urls
