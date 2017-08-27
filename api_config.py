#!/usr/bin/python
#-*-coding:utf-8-*-

import json
import logging

from constant import api_json


class ApiConfig(object):
    '''
    加载接口参数配置文件类
    '''

    def __init__(self, param_path=api_json):
        f = open(param_path, 'r')
        self.param_cfg = json.load(f)
        f.close()

    def get_param_dict(self, api_name):
        for p in self.param_cfg:
            if p['apiName'] == api_name:
                return p
        return None

    def find_api(self, api_name):
        for p in self.apis():
            if p['apiName'] == api_name:
                return p
        logging.warning('api: %s not found, check you config file'%api_name)
        return None

    def apis(self):
        return self.param_cfg
