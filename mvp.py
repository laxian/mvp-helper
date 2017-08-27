import sys

from api_config import ApiConfig
from myapi import ApiImpl
from constant import api_json
from task import TaskConfig, Task

man = '''

快速生成代码，根据配置，在制定位置插入代码
usage:
    python mvp.py [getUserInfo]

'''

if __name__=='__main__':

    api_cfg = ApiConfig(api_json)
    api_list = []
    if len(sys.argv) == 1:
        for da in api_cfg.apis():
            api_list.append(ApiImpl(da))
    else:
        api_name = sys.argv[1]
        api_dict = api_cfg.find_api(api_name)
        if api_dict:
            api = ApiImpl(api_dict)
            api_list.append(api)

    task_cfg = TaskConfig()
    tasks = task_cfg.tasks()

    for api in api_list:
        for t in tasks:
            task = Task(t, task_cfg.project_root(), api)
            task.exec()