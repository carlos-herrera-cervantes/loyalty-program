from rest_framework.routers import SimpleRouter
from django.urls import path

from .views.campaign_view import CampaignView
from .views.user_view import UserView
from .views.auth_view import AuthView
from .views.bucket_view import BucketView
from .views.customer_view import CustomerView
from .views.customer_keys_view import CustomerKeysView
from .views.organization_view import OrganizationView
from .views.operation_view import OperationView
from .views.action_view import ActionView
from .views.event_code_view import EventCodeView
from .views.task_view import TaskView

router = SimpleRouter()
router.register(r'api/v1/users', UserView)
router.register(r'api/v1/campaigns', CampaignView)
router.register(r'api/v1/buckets', BucketView)
router.register(r'api/v1/customers', CustomerView)
router.register(r'api/v1/customers-keys', CustomerKeysView)
router.register(r'api/v1/organizations', OrganizationView)
router.register(r'api/v1/operations', OperationView)
router.register(r'api/v1/actions', ActionView)
router.register(r'api/v1/event-codes', EventCodeView)
router.register(r'api/v1/tasks', TaskView)

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
