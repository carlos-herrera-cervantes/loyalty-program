from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import json

from config.app import AppConfig
from config.db import MongoClient
from routes.organization import organization_router
from routes.bucket import bucket_router
from routes.campaign import campaign_router
from routes.action import action_router
from routes.operation import operation_router
from routes.event_code import event_code_router
from routes.task import task_router
from routes.customer import customer_router
from routes.transaction import transaction_router

MongoClient().connect()
app = Sanic(AppConfig.NAME.value)

v1 = Blueprint.group(
    organization_router,
    bucket_router,
    campaign_router,
    action_router,
    operation_router,
    event_code_router,
    task_router,
    customer_router,
    transaction_router,
    url_prefix='/api/v1/program'
)
app.blueprint(v1)

@app.route('/')
async def health_check(req: Request) -> json:
    return json({
        'status': True,
        'message': 'Server is up',
    })

if __name__ == '__main__':
    reload: bool = AppConfig.ENVIRONMENT.value == 'DEV'

    app.run(
        host=AppConfig.HOST.value,
        port=AppConfig.PORT.value,
        debug=True,
        auto_reload=reload
    )
