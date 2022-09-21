import os
from enum import Enum


class AppConfig(Enum):
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    ENVIRONMENT = os.getenv('ENVIRONMENT')
    NAME = 'loyalty-program'
