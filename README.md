# KeanWISEcrawler

## 快速开始

快速抓取KeanWISE选课部分课程信息

#### 从requests开始：

安装下列依赖：

> requests
> 
> lxml
> 
> 本部分仍存问题，可能需要其他依赖

运行`req.py`文件即可获取json文件。

运行`reqcleaner.py` 完成数据清洗。对该文件改动可以调整需要的数据。

##### ***目前可以公布的情报(XD)***

在访问`Search`页面时，有一个发往`SearchSync` 的**POST请求**，携带了对应筛选条件的payload（`req.py`中的`payload`变量（打包为json发送））其返回值是包含了当前页面所有课程的所有信息的json对象。

这个POST请求在正常浏览器访问流程中是被一个js发起的。

## Todo：

- [ ] 上传清洗后的数据到数据库

- [ ] ~~建筑系课程STUDIO时段显示异常~~ （建筑系课程特殊暂不考虑）
