import requests
import json

# 这里header中应该包含了一个验证时间的cookie，每次需要获取信息之前手动登录一次，打开F12复制发送往
# https://selfservice.kean.edu/Student/Courses/SearchAsync
# 的Request headers，粘贴在下方即可。
# 注：快速添加单引号和逗号的方式：
# 打开替换功能(Ctrl + R)， 打开选区替换，选中headers选区，打开正则功能
# 查找栏：(.*?): (.*)
# 替换栏：'$1': '$2',


max_page_num = 24
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

# searchParameters内的pageNumber变量控制了当前页页码
for page_number in range(1, max_page_num + 1):
    payload = {"searchParameters":
                   "{\"keyword\":null,\"terms\":[\"22/SPWZ\"],\"requirement\":null,\"subrequirement\":null,"
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

    r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)
    print(r.content.decode(encoding='utf-8'))
    # 先保存后续在本地处理，不浪费时间，对这个cookie有心理阴影。
    with open(f'info/searchInfo_{page_number}.json', 'w+', encoding='utf-8') as file:
        file.write(r.content.decode(encoding='utf-8'))
