from typing import Iterable
from .models import *
from core.errors import APIError, Error


def get_config_with(key: str, type: str):
    try:
        value = Config.objects.get(key=key)
        if type.lower() == 'string':
            return value.value
        elif type.lower() == 'boolean':
            return value._boolean
        elif type.lower() == 'int':
            return value._int
        elif type.lower() == 'float':
            return value._float
        else:
            # This should not happen
            raise ValueError('You should pass a valid type.')
    except Config.DoesNotExist:
        # This should not happen
        raise ValueError('The key', key, 'does not have a value.')


def get_public_configs_by(tag: str) -> Iterable[Config]:
    return Config.objects.filter(tag=tag.lower(), is_private=False)


def get_public_config_by(key: str) -> Config:
    try:
        return Config.objects.get(key=key.upper(), is_private=False)
    except Config.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Config._meta.model_name])


def get_public_configs() -> Config:
    return Config.objects.filter(is_private=False)
