import json

max_page_num = 24


def get_course_info_list() -> list:
    course_info_list = []
    for page in range(1, max_page_num + 1):

        with open(f'info/searchInfo_{page}.json', 'r') as file:
            s = file.read()
            info = json.loads(s)

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
            }
            # print(page, formatted_course)
            course_info_list.append(formatted_course)
    return course_info_list
