import threading
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
import private

thread_lock = threading.Lock()  # Lock
info = {
    'username': private.username,
    'password': private.password,
    'term': 'Spring 2022 Wenzhou',
    'page#': 39,
}
pages = [False for j in range(info['page#'])]


def login(browser: webdriver.Chrome):
    browser.get('https://webreg.kean.edu/')

    try:
        time.sleep(7)
        login_button = browser.find_element(by="xpath",
                                            value="//body/div[@id='webPage']/div[@id='pageHeader']/div[@id='headerBanner']/div[@id='acctToolbar']/ul[1]/li[3]/a[1]/span[1]")
        login_button.click()

        time.sleep(2)
        username = browser.find_element(by='xpath',
                                        value="//input[@id='USER_NAME']")
        pwd = browser.find_element(by='xpath',
                                   value="//input[@id='CURR_PWD']")
        username.send_keys(info['username'])
        pwd.send_keys(info['password'])
        time.sleep(1)
        login_button = browser.find_element(by='xpath',
                                            value="//body/div[@id='webPage']/div[@id='pageBody']/div[@id='bodyForm']/div[4]/form[1]/div[1]/input[1]")
        login_button.click()
        time.sleep(3)
        student_menu = browser.find_element(by='xpath',
                                            value="//body/div[@id='webPage']/div[@id='mainBody']/div[@id='mainForm']/div[@id='mainMenu']/a[2]")
        student_menu.click()
    except NoSuchElementException:
        print('TOO SLOW LOADING')
        exit(-1)


def enter_course_page(browser: webdriver.Chrome):
    search_page = browser.find_element(by='xpath',
                                       value="//span[contains(text(),'Search for Course Sections')]")
    search_page.click()
    time.sleep(2)
    term_selector = Select(browser.find_element(by='xpath',
                                                value="//select[@id='VAR1']"))
    term_selector.select_by_visible_text(info['term'])

    weekday_selector_1 = browser.find_element(by='xpath',
                                              value="//label[@id='LABELID_VAR10']")
    weekday_selector_2 = browser.find_element(by='xpath',
                                              value="//label[@id='LABELID_VAR11']")
    weekday_selector_3 = browser.find_element(by='xpath',
                                              value="//label[@id='LABELID_VAR12']")
    weekday_selector_4 = browser.find_element(by='xpath',
                                              value="//label[@id='LABELID_VAR13']")
    weekday_selector_5 = browser.find_element(by='xpath',
                                              value="//label[@id='LABELID_VAR14']")

    weekday_selector_1.click()
    weekday_selector_2.click()
    weekday_selector_3.click()
    weekday_selector_4.click()
    weekday_selector_5.click()

    submit = browser.find_element(by='xpath',
                                  value="//body/div[@id='webPage']/div[@id='pageBody']/div[@id='bodyForm']/div[4]/form[1]/div[1]/input[1]")
    submit.click()


def save_page_source(browser: webdriver.Chrome, page_number):
    time.sleep(3)  # this loading is so long.
    jump_input = browser.find_element(by='xpath',
                                      value='/html/body/div/div[2]/div[4]/div[4]/form/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td[1]/input[5]')
    jump_input.send_keys(page_number)
    jump_btn = browser.find_element(by='xpath',
                                    value='/html/body/div/div[2]/div[4]/div[4]/form/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td[1]/input[6]')
    jump_btn.click()

    time.sleep(2)
    current_html = browser.page_source.encode('utf-8').decode()
    # print(current_html)
    course_page = open('pages/{}.html'.format(page_number), mode='w+', encoding='utf-8')
    course_page.write(current_html)


def find_uncollected_page():
    try:
        index = pages.index(False)
        return index + 1
    except ValueError:
        return -1


class SavingThread(threading.Thread):
    def __init__(self, name: str):
        threading.Thread.__init__(self)
        self.name = name
        self.pages = pages
        self.browser = webdriver.Chrome(service=Service(r"chromedriver_win32\chromedriver.exe"))
        self._flag = False

    def run(self):
        self.preparation()
        while self._flag is not True:
            page_number = self.update_page()
            if page_number is not None:
                print('Thread {} -- Collecting page {}'.format(self.name, page_number))
            else:
                print('Thread {} -- FINISHED'.format(self.name))
            self.work(page_number)

    def update_page(self):
        # CRITICAL
        thread_lock.acquire()
        page_number = find_uncollected_page()
        if page_number != -1:
            pages[page_number - 1] = True
            thread_lock.release()
            return page_number
        else:
            self._flag = True
            thread_lock.release()
            return None

    def preparation(self):
        login(self.browser)
        enter_course_page(self.browser)
        #  Wait for loading
        time.sleep(10)

    def work(self, page_number: int):
        if page_number is None:
            self._flag = True
            self.browser.close()
        else:
            save_page_source(self.browser, page_number)
