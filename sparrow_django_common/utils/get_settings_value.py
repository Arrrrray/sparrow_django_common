import os
from django.conf import settings


class GetSettingsValue(object):
    """settings数据"""

    def __get_settings_value(self, name):
        """获取settings中的配置， settings中数据"""
        value = getattr(settings, name, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % name)
        return value

    def __get_middleware_value(self, name):
        """
        获取中间件服务的配置数据,  PERMISSION_SERVICE 层数据， 
        PERMISSION_MIDDLEWARE = {
            "PERMISSION_SERVICE":{
                "name": "",
                "host": "",
                "port": 8001,
                "address": "",
            },
            "CONSUL": {
                "host": "",
                "port": ,
                },
            "FILTER_PATH" : ['']
        }
        """
        service_value = self.__get_settings_value("PERMISSION_MIDDLEWARE")
        value = service_value.get(name, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % name)
        return value

    def __get_middleware_service_value(self, service_name, key):
        """
        获取中间件中服务的具体配置的值, PERMISSION_SERVICE 下的 name 层数据
        PERMISSION_MIDDLEWARE = {
            "PERMISSION_SERVICE":{
                "name": "",
                "host": "",
                "port": 8001,
                "address": "",
            },
            "CONSUL": {
                "host": "",
                "port": ,
                },
            "FILTER_PATH" : ['']
        }


        """
        middleware_value = self.__get_middleware_value(service_name)
        value = middleware_value.get(key, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % service_name,key)
        return value
    
    def get_settings_value(self, name):
        """获取settings中的服务配置"""
        value = self.__get_settings_value(name)
        return value

    def get_middleware_value(self, name):
        """获取中间件服务的值"""
        value = self.__get_middleware_value(name)
        return value

    def get_middleware_service_value(self, service_name, key):
        """获取settings具体的服务的具体配置的值"""
        value = self.__get_middleware_service_value(service_name, key)
        return value