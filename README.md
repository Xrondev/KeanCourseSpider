# KeanCourseSpider
[简体中文](README.md) | [English](README-EN.md)  
一个从肯恩大学自助网站检索**所有**课程信息的脚本。
可以检索肯恩大学和温州肯恩大学的全部课程。  
此脚本是为学习目的而开发的。**不鼓励任何方式的滥用**

## 快速开始
这个脚本使用了requests和tqdm。首先你应该激活一个python环境（或使用全局环境），随后运行：
```shell
pip install -r requirements.txt
```

对于国内用户，你可能需要：
```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

随后你可以开始使用这个脚本：
```shell
python main.py [-h] [-y Y] [-t {SPWZ,FAWZ,WBWZ,SP,FA,WB}] [-out {cli,script,csv}] [-proxy PROXY]
```
例如，爬取23年温州春季课程输出到csv
```shell
python main.py -y 23 -t SPWZ -out csv
```

## 参数介绍

> optional arguments:  
  -h, --help            show this help message and exit  
  -y Y                  [2 digits or 4 digits] The term year you need, notice that usually the COMING semester and the Ended semesterare stored in the self service. For example, it is 23 Winter, only 22 summer and 23spring can be visited on the website  
  -t {SPWZ,FAWZ,WBWZ,SP,FA,WB}  
                        term choices. Term code ends with WZ stands for Wenzhou-Kean University coursestodo: the summer course code is missing (I cannot get it, it is winter now)Generate a Github issue if the summer come and you find it!       
  -out {cli,script,csv}  
                        output type, every choice will generate json file in info/ . "script" invoking custom script in custom_action.py with retrieved data  
  -proxy PROXY          proxy settings, ignore if you can connect to self services smoothly


-h: 显示帮助  
-y: 学年，2位或4位数字，例如23 （2023学年）  
-t: 学期，带WZ结尾的是温州肯恩大学，否则是美肯。SP为春季，FA为秋季，WB为冬季  
-out：指定输出的方式，默认打印到命令行  
-proxy: 启用代理，不填默认不启用，若本机已经打开代理软件请走代理  

## 输出到数据库 （自定义输出）
**您必须修改custom_action.py中的内容以满足您的要求**  
当`-out`参数定义为`custom`时，主程序将调用custom_action.py中的main方法。你可以在这里定义你的数据处理方式，例如统计，上传到数据库或筛选。
```shell
python main.py -y 23 -t SPWZ -out custom
```
custom_action.py:
```python
import pymysql

class custom:
    def __init__(self):
        con = pymysql.connect(host='localhost',
                        user='root',
                        password='xxx',
                        database='xxx'
                      )
        self.cursor = con.cursor()

    def main(self, course_info: list):
        # do something here
        # for example, upload to a database (this is just an example cannot directly copy and use)
        self.cursor.execute("INSERT INTO table VALUES (%s)" % (course_info['id']))
    def end(self):
        self.cursor.close()
```

