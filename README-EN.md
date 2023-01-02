# KeanCourseSpider
[简体中文](README.md) | [English](README-EN.md)  
A script to retrieve all the course information from self-service website of Kean University.
Working for both Kean University and Wenzhou-Kean University.  
This script was developed for Learning purpose. **No abuse is encouraged.**  
You may find some error prompt write in Chinese.
## Quick Start 
This script only used requests and tqdm. Activate a python environment, and then run:
```shell
pip install -r requirements.txt
```
Then you can start to use the script by running:
```shell
python main.py main.py [-h] [-y Y] [-t {SPWZ,FAWZ,WBWZ,SP,FA,WB}] [-out {cli,script,csv}] [-proxy PROXY]
```
## Arguments
> optional arguments:  
  -h, --help            show this help message and exit  
  -y Y                  [2 digits or 4 digits] The term year you need, notice that usually the COMING semester and the Ended semesterare stored in the self service. For example, it is 23 Winter, only 22 summer and 23spring can be visited on the website  
  -t {SPWZ,FAWZ,WBWZ,SP,FA,WB}  
                        term choices. Term code ends with WZ stands for Wenzhou-Kean University coursestodo: the summer course code is missing (I cannot get it, it is winter now)Generate a Github issue if the summer come and you find it!       
  -out {cli,script,csv}  
                        output type, every choice will generate json file in info/ . "script" invoking custom script in custom_action.py with retrieved data  
  -proxy PROXY          proxy settings, ignore if you can connect to self services smoothly

  
-h: Displays help  
-y: School year, two or four digits, such as 23 (school year 2023)  
-t: The semester ending with WZ is Wenzhou-Kean University, otherwise it is Kean. SP for spring, FA for autumn, WB for winter  
-out: specifies the output mode. By default, it is printed to the command line  
-proxy: Enables proxy. If no parameter is specified, this parameter is disabled by default. If the proxy software is enabled on the local device, use the proxy
## Custom output (Output to a database)
**YOU MUST modify the content in custom_action.py to meet your requirement**  
When the '-out' argument is defined to `custom`, the main program calls the main method in custom_action.py. Here you can define your data processing methods, such as statistics, uploading to a database or filtering.
```shell
python main.py -y 23 -t SPWZ -out custom
```
custom_action.py example:
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