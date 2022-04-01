import time

import cleaner
from SavingThread import SavingThread

THREAD_NUM = 5
thread_list = []


def run():
    start = time.time()
    for i in range(0, THREAD_NUM):
        thread = SavingThread(name=str(i))
        thread_list.append(thread)
        thread.start()

    for th in thread_list:
        th.join()

    end = time.time()
    return end - start


# print(run())

# result = cleaner.cleaner(24)
# for page in result:
#     for course in page:
#         print(course)
