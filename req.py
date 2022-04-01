import requests
from lxml import etree
import json

token_url = 'https://selfservice.kean.edu/Student/Student/Courses/Search'
get_token = requests.get(url=token_url, verify=False)
selector = etree.HTML(get_token.text)
hidden_input = selector.xpath('//body/input[1]')
print(hidden_input[0].get('value'))
request_verification_token = hidden_input[0].get('value')
url = 'https://selfservice.kean.edu/Student/Courses/SearchAsync'
headers = {
    '__RequestVerificationToken': "bK2emcc8Ffrt6kXuA5bk00LaYyTw-cDdMTpwiY9HqHK95EhCPDdbHoOAlEefG-0UmORewyROD0Z-SJRuOTLmTtqX4m1WkSub9JrGRyTj7Ns1",
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    # 'Content-Length': '765',
    'Content-Type': 'application/json, charset=UTF-8',
    'Cookie': f'_gcl_au=1.1.1753591641.1646135059; _ga=GA1.2.2106589013.1646135093; _fbp=fb.1.1646135096284.1221033039; _gid=GA1.2.1844402360.1647247593; __RequestVerificationToken_L1N0dWRlbnQ1={request_verification_token}; BE_CLA3=p_id%3DA42LJANPR464RL8R6L42JP8NAAAAAAAAAH%26bf%3Dd8f87247584a95f0e0106fa3ce452852%26bn%3D1%26bv%3D3.43%26s_expire%3D1647339371698%26s_id%3DA42LJANPR464RP48RRL2JP8NAAAAAAAAAH; studentselfservice_production_sfid=999U47Z45Q87; studentselfservice_production_AuthMethod=Forms; studentselfservice_production_0=CA28A8953E4C24A7DFCC15F29A9509A428C573413F63D1E299F1E5F8911DF373BCE43B03E47DC8C4302DF050A95FC28425B3E002D7AC0BB887B34D20361CAFF11FD8AA4BE8ECD093424D819CAB7CC1CCB4F3CA8ACB987C74D7A0D6E6B709AA3BD05DC9DB342A2CB4617368EF78200F0C158D3E7EF2D3FFC5D2EFDD74173B8F1B57229C62513981B0C583077AAB5C655567F4F91F41F6B00E4447639B1ADAC62FF03014D2D62EBF45BD9AB698C0D6DD56D9E7208503868E435C070DD23D7CADAF33412EB4B21C0F6368D49CDA192F5DBB4CBACDB6016A5506F1E6DB85EFDBB510FB6B174AD7B7BE765A6FAE01C70EE8CA2EA5CE4BF0AB84A64B414B3F607B76CFAB119A152E440A2408727808BAFC7FFB8814CB431CA0926AE3AE9E6D24A6E5703DA745B79010FBCC2A08AD6CFA57D41EE6CF6F32DDB448DEE0A6C179908D33EBE780AC7BA44258350C5D59385E3AE08232FD9DCAA98961AF0DC06AA9047DCDADFB25373154EDA7F4E8C450D4924B69D8E401494E02CE33A3DDCB7CFCBE1141A7FFB524AB8CA500435CF328757FE15454185CCC41C1F85573D1D8E45C8604579E78E8C82B7FBB9CCACDD3159C9D07ECDEC926C78635460A1FF8239E47432CBDCD829FBCDFBDB5CA5DE79F6662D0EF111FCD138D874FF693CA287227FA1EF58B2FAE61DCB6E97113B7850CDACD8CB64E76141490F36049AA536E85C94B9091E92D09519DFE6BB56D504AD68369419570251FC1C4F0991CC956267D4BDD7CBAB132B25ADD6CC57504120EE9FAE5ECF1C4A8D9BE6C8F2A80477E8D32E9FD20702BFFC4492934ED380FE11AD7EFB43F68EF40130319570DA9EEB8D7A9A211B6A47F8A74E065836AF997C47C2FE0EEB170AFB78EBB39A6FA472C4DC385A1460194AD913938EE35C22F199FCFDC61152B545EB945C9BCC86830F32660558BB35AF231C71B244D39119E9A793012677C7B3E432DAFB905DBC02950FA236932B794115B5663EE2DACA9A0D7C8C7169D89BFAECA1F294BF58BF3C7001D3E738C3D3B12DE536CE06D6E81D2D5554B350489DDD6FE1A5A786D789DA4FF757637EB345CCC67FE301245C5B806AFCBC05F1579A9FC596BB30EB79D66299CD9742C2AA634913DC88A44979F9D40E3106E42AABCB8582C22D293254DE97D9CBF6610B65AC6CEEA88',
    'Host': 'selfservice.kean.edu',
    'Origin': 'https://selfservice.kean.edu',
    'Referer': 'https://selfservice.kean.edu/Student/Courses/Search',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
get_token.headers['Referer'] = 'https://selfservice.kean.edu/Student/Courses/Search'
page_num = 1
# payload = {
#     'searchParameters':
#         {'keyword': 'null',
#          'terms': ['22/SPWZ'],
#          'requirement': 'null',
#          'subrequirement': 'null',
#          'courseIds': 'null',
#          'sectionIds': 'null',
#          'requirementText': 'null',
#          'subrequirementText': '',
#          'group': 'null',
#          'startTime': 'null',
#          'endTime': 'null',
#          'openSections': 'null',
#          'subjects': [],
#          'academicLevels': [],
#          'courseLevels': [],
#          'synonyms': [],
#          'courseTypes': [],
#          'topicCodes': [],
#          'days': ['1', '2', '3', '4', '5'],
#          'locations': [],
#          'faculty': [],
#          'onlineCategories': 'null',
#          'keywordComponents': [],
#          'startDate': 'null',
#          'endDate': 'null',
#          'startsAtTime': 'null',
#          'endsByTime': 'null',
#          'pageNumber': page_num,
#          'sortOn': 'SectionName',
#          'sortDirection': 'Ascending',
#          'subRequirementText': 'null',
#          'quantityPerPage': 30,
#          'openAndWaitlistedSections': 'null',
#          'searchResultsView': 'SectionListing'}
#
# }

payload = {"searchParameters":
               "{\"keyword\":null,\"terms\":[\"22/SPWZ\"],\"requirement\":null,\"subrequirement\":null,"
               "\"courseIds\":null,\"sectionIds\":null,\"requirementText\":null,\"subrequirementText\":\"\","
               "\"group\":null,\"startTime\":null,\"endTime\":null,\"openSections\":null,\"subjects\":[],"
               "\"academicLevels\":[],\"courseLevels\":[],\"synonyms\":[],\"courseTypes\":[],\"topicCodes\":[],"
               "\"days\":[\"1\",\"2\",\"3\",\"4\",\"5\"],\"locations\":[],\"faculty\":[],\"onlineCategories\":null,"
               "\"keywordComponents\":[],\"startDate\":null,\"endDate\":null,\"startsAtTime\":null,"
               "\"endsByTime\":null,\"pageNumber\":1,\"sortOn\":\"SectionName\",\"sortDirection\":\"Ascending\","
               "\"subRequirementText\":null,\"quantityPerPage\":30,\"openAndWaitlistedSections\":null,"
               "\"searchResultsView\":\"SectionListing\"} ",
           }

r = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)
print(r.content.decode(encoding='utf-8'))
