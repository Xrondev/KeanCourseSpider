# KeanWISEcrawler

## 快速开始

快速抓取KeanWISE选课部分课程信息

提供了两种实现思路：selenium模拟用户点击以及requests向服务器发送请求。

#### 从selenium开始【废弃，暂留备用】：

安装下列依赖：

> selenium
> 
> beautifulsoup4
> 
> pymysql（仅上传到数据库需要使用）

线程数`main.py line6`调整。

__注意： 你需要一个和你chrome版本相对应的webdriver，放置在`./chromedriver_win32`路径下__

在`private.py`配置用户名，数据库信息后即可（数据库及对应表需要提前建立）。

数据库表结构参照`cleaner.py` line87,88

#### 从requests开始：

安装下列依赖：

> requests
> 
> lxml
> 
> 本部分仍存问题，可能需要其他依赖

运行`req.py`文件即可。

## 问题

#### selenium实现【废弃，暂留备用】:

selenuim方式无法获取课程部分信息，comments部分的信息由js加载，需要点击后才会展示，如果每一个页面都要点击30次获取的话时间会非常长（点击没有做）。

基于老版本的爬虫修改而来，部分流程可以直接略过。

- [ ] 未获取课程全部信息（考虑模拟点击每一个more标签）

- [ ] 课程信息页面跳转似乎不正确（从第X页跳到X页）

- [ ] 流程可优化（无需从keanWISE登录进入，可以优化掉每一个线程登录的时间）

#### requests实现：

已经模拟了对应的`header` `request_verification_toekn` `payload` 但是网页返回值为`An error occured when processing your request`

- [x] __无法正确获取返回值__

- [ ] 处理返回值，筛选信息

- [ ] 未实现上传数据库部分 

##### ***目前可以公布的情报(XD)***

在访问`Search`页面时，有一个发往`SearchSync` 的**POST请求**，携带了对应筛选条件的payload（`req.py`中的`payload`变量（打包为json发送））其返回值是包含了当前页面所有课程的所有信息的json对象。

这个POST请求在正常浏览器访问流程中是被一个js发起的。

##### 可能存在的问题是：~~

- [ ] ~~没有正确完成SSL验证(HTTPS。 目前的爬虫关闭了验证，每次发送请求会有警告)~~

- [x] header内配置错误（可能与`request_verification_toekn`有关）

- [ ] ~~被反爬虫识别（某些参数未配置？）~~
