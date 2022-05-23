from enum import Enum


class Role(Enum):
    SUPER_ADMIN = 'SuperAdmin'
    READER = 'Reader'


class Ability(Enum):
    READ_USERS = 'read.users'
    CREATE_USERS = 'create.users'
    UPDATE_USERS = 'update.users'
    DELETE_USERS = 'delete.users'
