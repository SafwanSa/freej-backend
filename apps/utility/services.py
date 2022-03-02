from . import queries
from .models import *

class ConfigService:
    @staticmethod
    def ACTIVATE_SMS():
        return bool(queries.get_config_with(
            key="ACTIVATE_SMS",
            type='boolean'
        ))
        
    @staticmethod      
    def TWITTER_LINK():
        return str(queries.get_config_with(
            key="TWITTER_LINK",
            type='string'
        ))
        
    @staticmethod
    def WHATSAPP_LINK():
        return str(queries.get_config_with(
            key="WHATSAPP_LINK",
            type='string'
        ))
        
    @staticmethod
    def IOS_APP_LINK():
        return str(queries.get_config_with(
            key="IOS_APP_LINK",
            type='string'
        ))
        
    @staticmethod
    def ANDROID_APP_LINK():
        return str(queries.get_config_with(
            key="ANDROID_APP_LINK",
            type='string'
        ))
        
    @staticmethod
    def WEBSITE_URL():
        return str(queries.get_config_with(
            key="WEBSITE_URL",
            type='string'
        ))
        
    @staticmethod
    def ACTIVATE_EMAILS():
        return bool(queries.get_config_with(
            key="ACTIVATE_EMAILS",
            type="boolean"
        ))