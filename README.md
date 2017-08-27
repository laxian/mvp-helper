# MVP helper
## 自动生成mvp框架代码

>之前写过一个[auto-mvp](https://github.com/laxian/auto-mvp)项目，和这个是一样的东东，只不过之前的代码太具体，难以移植。我在两个项目中使用，但是这两个项目创建的
时间不同，虽然都是MVP结构，但是差异挺大，导致mvp一直到另一个上，相当于重写了一套。所以，我将与具体细节无关的操作提取了出来
对于一个项目，花一点点时间配置一下，能节省不少时间

#### 思路

对于一些有规律的代码，根据事先准备好的模板，**替换**其中的变量，生成代码。
生成的代码，或者需要**插入**某些文件中的指定位置，或者需要**生成文件**并写入


> 插入代码
       通过正则表达式匹配插入代码的开始行，通过'{'和'}'对查找当前代码块结束的行，并在结束行前插入代码
       代码插入前代码重复判断，如果当前行已存在，跳过


#### 使用

实现class Api 中的两个方法

```
	class Api(object):

	            def __init__(self):
	                pass

	            @abc.abstractclassmethod
	            def holder_list(self):
	                pass

	            @abc.abstractclassmethod
	            def key_list(self):
	                pass
```

配置文件

+ api配置文件

   声明了api的一些基本信息，下面的sample包含了所有支持的配置
    method: 请求方法
    path:   方法名上一级路径，可选
    apiName:请求函数名
    bean:   对应bean类
    parent: page上一层目录，可选
    page:   所在页面
    alias:  别名，默认为page，可选
    params: 请求参数列表

```
        [
             {
               "method": "get",
               "path": "t",
               "apiName": "modifyTeacherInfo",
               "bean": "GetTeacherSignatureData",
               "page": "classinfo",
               "parent": "teach",
               "params": {
                 "userId": "int",
                 "pageNum": "int",
                 "pageSize": "int",
                 "time": "long",
                 "sign": "String"
               }
             },
             {
               "method": "post",
               "path": "t",
               "apiName": "getTeacherInfo",
               "bean": "GetTeacherInfoData",
               "parent": "teach",
               "page": "classhome",
               "alias": "class",
               "params": {
                 "userId": "int",
                 "time": "long",
                 "sign": "String"
               }
             }
           ]

```

+  操作配置

   root_project    项目根目录
   tasks:          对于每一个api，进行的操作
       path:       需要插入或者创建的文件，路径中的关键字会被替换
       create_if_not_exists:   如果文件不存在，是否创建
       template:               如果文件不存在，create_if_not_exists 为true，则根据模板创建文件，模板中的关键字会被替换
       inserts                 插入列表，每一项代表一个插入点，可能插入多行。插入位置在当前代码块结束'}'前一行
           regex:              正则表达式，匹配插入代码块开始位置
           lines:              需要插入的行，行中的关键字会被替换


```
{
         "project_root": "/Users/leochou/StudioProjects/DywTeacher/",
         "tasks": [
           {
             "path": "app/src/main/java/com/etiantian/dywteacher/ui/teach/{page}/{Alias}Contract.java",
             "create_if_not_exists": true,
             "template": "/Users/leochou/PycharmProjects/mvp-helper/template/SampleContract.java",
             "inserts": [
               {
                 "regex": " *interface Model extends IBaseModel \\{\n",
                 "lines": [
                   {
                     "line": "\t\tObservable<Result<{Bean}>> {apiName}({TypedParams});\n"
                   }
                 ]
               },
               {
                 "regex": " *interface View extends IBaseView \\{\n",
                 "lines": [
                   {
                     "line": "\t\tvoid on{ApiName}Success({Bean} data);\n"
                   }
                 ]
               },
               {
                 "regex": " *abstract class Presenter extends BasePresenter<Model, View> \\{\n",
                 "lines": [
                   {
                     "line": "\t\tabstract void {apiName}({TypedParams});\n"
                   }
                 ]
               }
             ]
           },
           {
             "path": "app/src/main/java/com/etiantian/dywteacher/ui/teach/{page}/{Alias}Model.java",
             "create_if_not_exists": true,
             "template": "/Users/leochou/PycharmProjects/mvp-helper/template/SampleModel.java",
             "inserts": [
               {
                 "regex": "public class .+?Contract.Model \\{\n",
                 "lines": [
                   {
                     "line": "\n    @Override\n    public Observable<Result<{Bean}>> {apiName}({TypedParams}) {\n        return Networks.getInstance().getCommonApi()\n                .{apiName}(getParams(Constants.Http.KEY_{API_NAME}\n                        {ParamsPair})).compose(RxSchedulerHelper.<Result<{Bean}>>io_main());\n    }\n"
                   }
                 ]
               }
             ]
           },
           {
             "path": "app/src/main/java/com/etiantian/dywteacher/ui/teach/{page}/{Alias}Presenter.java",
             "create_if_not_exists": true,
             "template": "/Users/leochou/PycharmProjects/mvp-helper/template/SamplePresenter.java",
             "inserts": [
               {
                 "regex": "public class .+?Contract.Presenter \\{\n",
                 "lines": [
                   {
                     "line": "    \n    @Override\n    void {apiName}({TypedParams}) {\n        mRxManager.add(mModel.{apiName}({params})\n                .map(new RxFunc.ServerResultFunc<{Bean}>())\n                .onErrorResumeNext(new RxFunc.HttpResultFunc<{Bean}>())\n                .subscribe(new FilterSubscriber<{Bean}>(mView) {\n\n                    @Override\n                    public void onNext({Bean} data) {\n                        mView.on{ApiName}Success(data);\n                    }\n                }));\n    }\n"
                   }
                 ]
               }
             ]
           },
           {
             "path": "app/src/main/java/com/etiantian/dywteacher/api/CommonApi.java",
             "inserts": [
               {
                 "regex": "public interface CommonApi {",
                 "lines": [
                   {
                     "line": "\n\t@{METHOD}(Constants.Http.URL_{API_NAME})\n    Observable<Result<{Bean}>> {apiName}({retrofitParams});\n"
                   }
                 ]
               }
             ]
           },
           {
             "path": "app/src/main/java/com/etiantian/dywteacher/global/Constants.java",
             "inserts": [
               {
                 "regex": " *public interface Http \\{",
                 "lines": [
                   {
                     "line": "\n\t\tString {PATH} = \"{path}/\";\n"
                   },
                   {
                     "line": "\n\t\tString KEY_{API_NAME} = \"{apiName}.do\";\n"
                   },
                   {
                     "line": "\t\tString URL_{API_NAME} = {PATH} + KEY_{API_NAME};\n"
                   }
                 ]
               }
             ]
           }
         ]
       }
```