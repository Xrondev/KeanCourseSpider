# *******Coding: UTF-8*******
# Developer : Elysium
# Develop Time : 4/11/2021 下午3:04
# File Name : cleaner.py
# Developed by PyCharm
import re
import private
import pymysql
from bs4 import BeautifulSoup

page_number = 24
db = private.db


def cleaner(page_number):
    current_page = 1
    results = []
    # while current_page <= page_number:
    file = open('pages/{}.html'.format(current_page), mode='r', encoding='utf-8')
    soup = BeautifulSoup(file, features='html.parser')

    term = soup.find_all(name='td', id=re.compile(r'term-[\d]'))
    status = soup.find_all(name='td', id=re.compile(r'availability-status-[\d]'))
    section_name = soup.find_all(name='td', attrs={'data-role': 'Section Name'})
    title = soup.find_all(name='td', attrs={'data-role': 'Title'})
    # planned_status = soup.find_all(name='td', attrs={'data-role': 'Planned Status'})
    dates = soup.find_all(name='td', attrs={'data-role': 'Dates'})
    location = soup.find_all(name='td', attrs={'data-role': 'Location'})
    instruction_methods = soup.find_all(name='td', attrs={'data-role': 'Instructional Methods'})
    meetings = soup.find_all(name='td', attrs={'data-role': 'Meetings'})
    faculty = soup.find_all(name='td', attrs={'data-role': 'Faculty'})
    availability = soup.find_all(name='td', attrs={'data-role': 'Availability'})
    credits = soup.find_all(name='td', attrs={'data-role': 'Credits'})
    course_types = soup.find_all(name='td', attrs={'data-role': 'Course Types'})
    academic_level = soup.find_all(name='td', attrs={'data-role': 'Academic Level'})
    comments = soup.find_all(name='td', attrs={'data-role': 'Comments'})
    book_store = soup.find_all(name='td', attrs={'data-role': 'Book Store'})

    # todo: 要获取comment内的内容

    # index = soup.find_all(name='td', attrs={'class': 'windowIdx'})
    # term = soup.find_all(name='p', id=re.compile(r'WSS_COURSE_SECTIONS_[1\d]'))
    # status = soup.find_all(name='p', id=re.compile(r'LIST_VAR1_[1\d]'))
    # title = soup.find_all(name='a', id=re.compile(r'SEC_SHORT_TITLE_[1\d]'))
    # location = soup.find_all(name='p', id=re.compile(r'SEC_LOCATION_[1\d]'))
    # sections = soup.find_all(name='p', id=re.compile(r'LIST_VAR10_[1\d]'))
    # faculty = soup.find_all(name='p', id=re.compile(r'SEC_FACULTY_INFO_[1\d]'))
    # capacity = soup.find_all(name='p', id=re.compile(r'LIST_VAR5_[1\d]'))
    # credits_ = soup.find_all(name='p', id=re.compile(r'SEC_MIN_CRED_[1\d]'))
    # frequency = soup.find_all(name='p', id=re.compile(r'VAR_SEC_YEARLY_CYCLE_[1\d]'))
    # level = soup.find_all(name='p', id=re.compile(r'SEC_ACAD_LEVEL_[1\d]'))
    # pre_requisites = soup.find_all(name='p', id=re.compile(r'LIST_VAR13_[1\d]'))
    print(term[0].div.text, status[0].text, section_name[0].div.a.text, title[0].div.text, dates[0].div.text,
          location[0].div.text, instruction_methods[0].div.text, meetings[0].div.text.strip(), faculty[0].div.text.strip(),
          availability[0].div.text, credits[0].div.text, course_types[0].div.text, academic_level[0].div.text,
          comments[0].div.text)

#     for item in range(0, len(index)):
#         _index = index[item].contents
#         _term = term[item].contents
#         _status = status[item].contents
#         _title = title[item].contents
#         _location = location[item].contents
#         _sections = sections[item].contents
#         _faculty = faculty[item].contents
#         _capacity = capacity[item].contents
#         _credits = credits_[item].contents
#         _frequency = frequency[item].contents
#         _level = level[item].contents
#         _pre_requisites = pre_requisites[item].contents
#         results.append(
#             [_index[0], _term[0], _status[0], _title[0], _location[0], _sections[0], _faculty[0], _capacity[0],
#              _credits[0], _frequency[0],
#              _level[0],
#              _pre_requisites[0]])
#
#     current_page += 1
# return results

cleaner(1)


def send_db(data):
    conn = pymysql.connect(host=db['host'], port=db['port'], db=db['db'], user=db['usr'], password=db['pwd'])
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    for i in data:
        sql = "insert into " + db[
            'table'] + "( index_in_form, term, status, title, location, sections, faculty, capacity, credits, frequency, level, pre_requisites) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
        params = (
            int(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7]), str(i[8]),
            str(i[9]),
            str(i[10]), str(i[11]))

        cursor.execute(sql, params)
    # 查看结果
    cursor.close()
    conn.commit()
    conn.close()

# result = cleaner(page_number)
# send_db(result)

# class CleaningThread(threading.Thread):
#     def run(self):
#         pass
#
#     def work(self, page_number):
#         result = cleaner(page_number)
#         return result
