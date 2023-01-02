import os
import sys
import argparse
import requests
import json
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()
# --------- 自新系统（self-service）启用后不再需要更换header -------------
# --------- 使用固定的header即可获取到相关数据 -------------


url = 'https://selfservice.kean.edu/Student/Courses/SearchAsync'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '791',
    'Content-Type': 'application/json, charset=UTF-8',
    'Cookie': '_gcl_au=1.1.1753591641.1646135059; _ga=GA1.2.2106589013.1646135093; _fbp=fb.1.1646135096284.1221033039; BE_CLA3=p_id%3DA42LJANPR464RL8R6L42JP8NAAAAAAAAAH%26bf%3Dd8f87247584a95f0e0106fa3ce452852%26bn%3D1%26bv%3D3.43%26s_expire%3D1647339371698%26s_id%3DA42LJANPR464RP48RRL2JP8NAAAAAAAAAH; _gid=GA1.2.1325093295.1648733476; __RequestVerificationToken_L1N0dWRlbnQ1=KvZJFlCnwJzVSeUopSzqV9vJcjbZHW5zaDhKuZ1QvFkKZXbn4P7nrLFGPNh6fyoN7IcAa1pbAJc4GMhmom_XzpWbC44f5sLlybBOcYtnurs1',
    'Host': 'selfservice.kean.edu',
    'Origin': 'https://selfservice.kean.edu',
    'Referer': 'https://selfservice.kean.edu/Student/Courses/Search',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    '__RequestVerificationToken': 'Tc2UslJtK2j0UsTfG1OlTLn26pdZOKxVSij-38RnLiA_vyC365qkbmfzgyawns1zm8lVjsUyCqNi0BZmfUG-gV3oWe9oTJnl1Hkjrz2Dsrw1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

parser = argparse.ArgumentParser(description='''
A CLI tool retrieving all course data in Kean and Wenzhou-Kean University
''')

parser.add_argument('-y', type=int,
                    help='[2 digits or 4 digits] The term year you need, notice that'
                         ' usually the COMING semester and the Ended semester'
                         'are stored in the self service. For example, it is 23 Winter, only 22 summer and 23'
                         'spring can be visited on the website')
parser.add_argument('-t', choices=['SPWZ', 'FAWZ', 'WBWZ', 'SP', 'FA', 'WB'],
                    help='term choices. Term code ends with WZ stands for Wenzhou-Kean University courses'
                         'todo: the summer course code is missing (I cannot get it, it is winter now)'
                         'Generate a Github issue if the summer come and you find it!')
parser.add_argument('-out', choices=['cli', 'script', 'csv'], default='cli',
                    help='output type, every choice will generate json file in info/ '
                         '. "script" invoking custom script in custom_action.py '
                         'with retrieved data')

parser.add_argument('-proxy', type=str, help='proxy settings, ignore if you can connect to self services smoothly')




def main(year: int, semester: str, proxy: str) -> None:
    if len(str(year)) == 4:
        year = str(year)[-2:]

    term = f'{year}/{semester}'
    print('目标学期代码：', term)

    proxies = {
        'https': ''
    }
    if proxy:
        proxies['https'] = proxy
    else:
        proxies = {}
    # searchParameters内的pageNumber变量控制了当前页页码
    max_page_number = 1  # 第一次运行后自动获取最大页码
    page_number = 1
    with tqdm(unit='page') as pbar:
        while page_number <= max_page_number:
            payload = {"searchParameters":
                           "{\"keyword\":null,\"terms\":[\"" + term + "\"],\"requirement\":null,\"subrequirement\":null,"
                                                                      "\"courseIds\":null,\"sectionIds\":null,\"requirementText\":null,\"subrequirementText\":\"\","
                                                                      "\"group\":null,\"startTime\":null,\"endTime\":null,\"openSections\":null,\"subjects\":[],"
                                                                      "\"academicLevels\":[],\"courseLevels\":[],\"synonyms\":[],\"courseTypes\":[],\"topicCodes\":[],"
                                                                      "\"days\":[\"1\",\"2\",\"3\",\"4\",\"5\"],\"locations\":[],\"faculty\":[],\"onlineCategories\":null,"
                                                                      "\"keywordComponents\":[],\"startDate\":null,\"endDate\":null,\"startsAtTime\":null,"
                                                                      f"\"endsByTime\":null,\"pageNumber\": {page_number},\"sortOn\":\"SectionName\","
                                                                      "\"sortDirection\":\"Ascending\", "
                                                                      "\"subRequirementText\":null,\"quantityPerPage\":30,\"openAndWaitlistedSections\":null,"
                                                                      "\"searchResultsView\":\"SectionListing\"} "
                       }

            try:
                r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False, proxies=proxies)
                # print(r.content.decode(encoding='utf-8'))
                data = json.loads(r.content.decode(encoding='utf-8'))
                # print(data['TotalPages'])

                max_page_number = data['TotalPages']
                pbar.total = max_page_number
                # 更新最大页码数
                # print(f'Current/Total page: {page_number}/{max_page_number} ')
            except TypeError:
                print('学期或学年配置出错，获取不到课程')
                print(r.content.decode(encoding='utf-8'))
                sys.exit(-1)
            except Exception as e:
                print('连接出错，请检查网络或代理配置: \n', e)
                sys.exit(-1)

            with open(f'info/searchInfo_{page_number}.json', 'w+', encoding='utf-8') as file:
                file.write(r.content.decode(encoding='utf-8'))

            page_number += 1
            pbar.update(1)


def get_course_info_list(info: dict) -> list:
    # 有些课程可能有不止一种教学方式，对应了不止一套上课时间，例如物化生以及建筑系的STU工作室时段
    # 返回一个dict包含该课程的上课时段， 在该字典中，days和time都是列表，对应index上的数据表明对应工作日的上课时段
    # !!!注意： 建筑系的STU无法通过课程的Days，StartTime等字段获取，建筑系的课程会出现days中有一个空子列表，time中有一个[None, None]的子列表
    # 建筑系课程工作室时段无法正常显示。建筑系课程特殊，暂不考虑。
    def get_meeting_info(course_info: dict) -> dict:
        days = []
        time = []
        res = {
            'days': days,
            'time': time,
        }
        for meeting_time in course_info['FormattedMeetingTimes']:
            res['days'].append(meeting_time['Days'])
            start = meeting_time['StartTime']
            end = meeting_time['EndTime']
            res['time'].append([start, end])
        return res

    course_info_list = []

    for course in info['Sections']:
        meeting_info = get_meeting_info(course)
        formatted_course = {
            'id': int(course['Synonym']),  # 课程id，是指代该Section的唯一序列
            'term': str(course['TermDisplay']),  # 课程学期，形如 'Spring 2022 Wenzhou'
            'name': str(course['Course']['SubjectCode'] + '_' + course['Course']['Number']),  # 课程名称，形如 'ACCT_2210'
            'title': str(course['Course']['Title']),  # 课程标题，形如 'PRINCIPLES OF ACCOUNTING II'
            'section': str(course['Number']),  # 课程班级号，形如 'W01'
            'prof': str(course['FacultyDisplay']),  # 列表！教授名称（可能不止一个人）
            'days': str(meeting_info['days']),  # 形如[[1,3],[2]]，课程所在的工作日顺序，1对应星期一
            'time': str(meeting_info['time']),  # 形如[['16:00:00', '17:15:00'], ['08:30:00', '11:15:00']], 对应工作日的上课时间
            'description': str(course['Course']['Description']),  # 课程描述
            'comments': str(course['Comments']),  # 课程备注，非常重要！包含了对专业的限制
            'capacity': str(course['Capacity']),  # 容量
            'enrolled': str(course['Enrolled'])  # 已注册学生量
        }
        # print(page, formatted_course)
        course_info_list.append(formatted_course)
    return course_info_list


if __name__ == '__main__':

    if os.path.exists('./info'):
        print('移除缓存的json文件')
        for file in os.listdir('./info/'):
            os.remove(f'./info/{file}')
    args = parser.parse_args()
    term = args.t
    year = args.y
    proxy = args.proxy
    out = args.out
    main(args.y, args.t, args.proxy)

    course_info_list = []
    for info in os.listdir(r'./info'):
        with open('./info/' + info, 'r', encoding='utf-8') as file:
            s = file.read()
            info = json.loads(s)
            course_info_list.extend(get_course_info_list(info))

    if out == 'script':
        from custom_action import custom
        c = custom()
        with tqdm(len(course_info_list), unit='') as pbar:
            for course in course_info_list:
                c.main(course)
                pbar.update(1)
        c.end()
    elif out == 'csv':
        with open('./course_list.csv', 'w+', encoding='utf-8') as f:
            with tqdm(len(course_info_list), unit='') as pbar:
                for info in course_info_list:
                    for i in info:
                        f.write(f'"{str(info[i]).strip()}",')
                    f.write('\n')
                    pbar.update(1)
    elif out == 'cli':
        for info in course_info_list:
            print(info)
