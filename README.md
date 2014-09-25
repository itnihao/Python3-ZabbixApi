Python3-ZabbixApi
=================

https://www.zabbix.com/documentation/2.4/manual/api

example:

import ZabbixApi

params_host_get = {
                  "output": "extend",
                  "filter": {
                            "host": [
                                    "Zabbix server",
                                    "Linux server"
                                    ]
                            }
                  }

zapi = ZabbixApi.ZabbixApi(host='127.0.0.1', user='Admin', password='zabbix')

retval = zapi.host.get(params_host_get)

print(retval)
