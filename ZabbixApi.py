#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: xinxin.xu
# mail: uininx@126.com

import http.client
import json

def wrap(fn):
    def wrapped(self, body):
        retval = fn(self, body)
        return retval
    return wrapped

class ZabbixApiException(Exception):
    pass

class ZabbixApi(object):
    __id = 0
    __auth = ''
    
    def __init__(self, host='127.0.0.1', user='Admin', password='zabbix', url='/api_jsonrpc.php', jsonrpc='2.0', headers={"Content-Type": "application/json"}):
        self.__url = url
        self.__jsonrpc = jsonrpc
        self.__headers = headers
        self.__host = host
        self.__user = user
        self.__password = password
        self.__zabbix_api_object_list = ('action', 'alert', 'apiinfo', 'application', 'configuration', 'dcheck', 'dhost', 'discoveryrule', 'drule', 'dservice',
                'event', 'graph', 'graphitem', 'graphprototype', 'history', 'host', 'hostgroup', 'hostinterface', 'hostprototype', 'httptest', 'iconmap',
                'image', 'item', 'itemprototype', 'maintenance', 'map', 'mediatype', 'proxy', 'screen', 'screenitem', 'script', 'service', 'template',
                'templatescreen', 'templatescreenitem', 'trigger', 'triggerprototype', 'user', 'usergroup', 'usermacro', 'usermedia')
        self.__conn = http.client.HTTPConnection(self.__host)
        self.login_Zabbix()

    def __getattr__(self, name):
        if name not in self.__zabbix_api_object_list:
            raise ZabbixApiException('No such API object: %s' % name)
        if name not in self.__dict__:
            self.__dict__[name] = ZabbixApiObjectFactory(self, name)
        return self.__dict__[name]
    
    def login_Zabbix(self):
        json_request_object = self.json_Request_Object('user', 'login', {'user':self.__user, 'password':self.__password})
        retval = self.request_Zabbix(json_request_object)
        if 'error' in retval:
            raise ZabbixApiException(retval)
        self.__auth = retval['result']
    
    def json_Request_Object(self, object_name, object_method, params):
        method = "%s.%s" % (object_name, object_method)
        if method == 'user.login':
            request_object = {
                              "jsonrpc" : self.__jsonrpc,
                              "method" : method,
                              "params" : params,
                              "id": self.__id,
                              }
        else:
            request_object = {
                              "jsonrpc" : self.__jsonrpc,
                              "method" : method,
                              "params" : params,
                              "id": self.__id,
                              "auth": self.__auth
                              }
        json_request_object = json.dumps(request_object)
        return json_request_object
    
    @wrap
    def request_Zabbix(self, body):
        self.__conn.request('POST', self.__url, body, self.__headers)
        response = json.loads(self.__conn.getresponse().read().decode('utf-8'))
        self.__id += 1
        return response
    
class ZabbixApiObjectFactory(object):
    def __init__(self, zapi, object_name=''):
        self.__zapi = zapi
        self.__object_name = object_name
    def __checkAuth__(self):
        self.__zapi.__checkAuth__()
    def __getattr__(self, object_name):
        def func(params):
            json_request_object = self.__zapi.json_Request_Object(self.__object_name, object_name, params)
            response = self.__zapi.request_Zabbix(json_request_object)
            return response
        return func

def test():
    pass

if __name__ == '__main__':
    test()
