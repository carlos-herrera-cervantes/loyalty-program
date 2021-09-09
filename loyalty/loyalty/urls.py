from rest_framework.routers import SimpleRouter
from django.urls import path

from .views.campaign_view import CampaignView
from .views.user_view import UserView
from .views.auth_view import AuthView
from .views.bucket_view import BucketView
from .views.customer_view import CustomerView
from .views.customer_keys_view import CustomerKeysView

router = SimpleRouter()
router.register(r'api/v1/users', UserView)
router.register(r'api/v1/campaigns', CampaignView)
router.register(r'api/v1/buckets', BucketView)
router.register(r'api/v1/customers', CustomerView)
router.register(r'api/v1/customers-keys', CustomerKeysView)

sign_in = AuthView.as_view({'post': 'sign_in'})
logout = AuthView.as_view({'post': 'logout'})
sign_up_user = AuthView.as_view({'post': 'sign_up_user'})
sign_up_customer = AuthView.as_view({'post': 'sign_up_customer'})

urlpatterns = [
    path(r'api/v1/auth/sign-in', sign_in),
    path(r'api/v1/auth/logout', logout),
    path(r'api/v1/customers/sign-up', sign_up_customer),
    path(r'api/v1/users/sign-up', sign_up_user)
]

urlpatterns += router.urls
