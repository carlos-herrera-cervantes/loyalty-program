from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from config.app import AppConfig

app = Sanic(AppConfig.NAME.value)

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
        reload=reload
    )
