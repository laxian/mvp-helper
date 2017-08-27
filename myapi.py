#!/usr/bin/python
# -*-coding:utf-8-*-

import json

import utils
import logging

from api import Api


class ApiImpl(Api):
    '''
    {alias}、{Bean}、{TypedParams}、{ParamsPair}、{ApiName}、{apiName}、{API_NAME}
    '''

    def __init__(self, param, exclude=None):
        super().__init__()
        if exclude is None:
            exclude = ['time', 'sign', 'userId']
        self.exclude = exclude
        if isinstance(param, str):
            self.param = json.loads(param)
        elif isinstance(param, dict):
            self.param = param
        else:
            logging.error('\tApi.__init__:  param is %r' % type(param))
            exit(-1)

    def holder_list(self):
        return ['{Alias}',
                '{page}',
                '{Bean}',
                '{TypedParams}',
                '{ParamsPair}',
                '{params}',
                '{ApiName}',
                '{apiName}',
                '{API_NAME}',
                '{METHOD}',
                '{retrofitParams}',
                '{path}',
                '{PATH}']

    def key_list(self):
        return [
            self.Alias(),
            self.page(),
            self.bean(),
            self.typed_params(),
            self.params_pair(),
            self.params_split(),
            self.ApiName(),
            self.apiName(),
            self.API_NAME(),
            self.method().upper(),
            self.retrofit_params(),
            self.path(),
            self.PATH()
        ]

    def page(self):
        return self.param['page']

    def bean(self):
        return self.param['bean']

    def typed_params(self):
        '''
        input:
          "userId": "int",
          "studentId": "int",
          "time": "long",
          "sign": "String"
        :return: int userId,int studentId,long time,String sign
        '''
        lst = []
        pdic = self.params()
        for k, v in pdic.items():
            if k not in self.exclude:
                lst.append('%s %s' % (v, k))
        return ', '.join(lst)

    def params_pair(self):
        '''
        input:
          "userId": "int",
          "studentId": "int",
          "time": "long",
          "sign": "String"
        :return:
        '''
        lst = []
        for k, v in self.params().items():
            if k not in self.exclude:
                lst.append('"%s", %s' % (k, k))
        if lst:
            lst.insert(0, '')
        return ','.join(lst)

    def apiName(self):
        return self.param['apiName']

    def ApiName(self):
        return self.param['apiName'].capitalize()

    def API_NAME(self):
        return '_'.join([w.upper() for w in utils.split_camel(self.param['apiName'])])

    def method(self):
        return self.param['method']

    def path(self):
        return self.param['path']

    def PATH(self):
        return self.param['path'].capitalize()

    def params(self):
        return self.param['params']

    def param_list(self):
        return list(self.param['params'].keys())

    def parent(self):
        return self.param['parent'] if self.param['parent'] else ''

    def params_split(self):
        lst = [w for w in self.params() if w not in self.exclude]
        return ','.join(lst)

    def Alias(self):
        ret = self.param['alias'] if 'alias' in self.param else self.page()
        return ret.capitalize()

    def retrofit_params(self):
        if self.method().lower() == 'get':
            return '@QueryMap Map<String, String> params'
        elif self.method().lower() == 'post':
            return '@FieldMap Map<String, String> params'


if __name__ == '__main__':
    api = '''{
        "method": "get",
        "path": "classm",
        "apiName": "getUpClassInfo.do",
        "params": {
          "userId": "int",
          "classId": "int",
          "time": "long",
          "sign": "String"
        }
      }
    '''

    a = ApiImpl(api)
    print(a)
    print(a.apiName())
    print(a.method())
    print(a.path())
    print(a.params())
    print(a.param_list())
