import json
import os

import utils
from constant import task_json


class TaskConfig(object):
    def __init__(self, config=task_json):
        if os.path.exists(task_json):
            self.tdic = json.loads(open(task_json).read())

    def project_root(self):
        return self.tdic['project_root']

    def tasks(self):
        return self.tdic['tasks']


class Task(object):
    def __init__(self, dic, root, api):
        self.root = root
        self.api = api
        if isinstance(dic, dict):
            self.dic = dic
        elif isinstance(dic, str):
            self.dic = json.loads(dic)
        else:
            print('error task config')

    def path(self):
        raw = self.dic['path']
        return self.root + self._replace(raw)

    def create_if_not_exists(self):
        return self.dic['create_if_not_exists']

    def template(self):
        return self.dic['template']

    def inserts(self):
        if 'inserts' not in self.dic:
            print('no task find')
            return None
        return self.dic['inserts']

    def exec(self):
        inserts = self.inserts()
        if not self.inserts():
            return
        path = self.path()
        if not os.path.exists(path):
            if not self.create_if_not_exists():
                print('%s not exists. do you forgot create_if_not_exists in task config?'%path)
                return
            # 从模板读取，关闭
            template=self.template()
            f=open(template)
            content=f.read()
            f.close()
            # 替换所有占位符
            new_content = self._replace(content)
            # 创建输入文件，写入，关闭
            fo = open(path, 'w+')
            fo.write(new_content)
            fo.close()
        else:
            # 文件存在，则插入。读取插入位置，和插入行列表。1对多
            reglist, lineslist = [], []
            for ins in inserts:
                # 一个插入点,可插入1+行
                regex = ins['regex']
                lines = ins['lines']

                llst = []
                for d in lines:
                    l=d['line']
                    l = self._replace(l)
                    llst.append(l)

                reglist.append(regex)
                lineslist.append(llst)
            utils.insert_all(path, reglist, lineslist)

    def _replace(self, content):
        return utils.replace_holder(content, self.api.holder_list(), self.api.key_list())
