from gevent import monkey; monkey.patch_all()
import gevent
from tornado.queues import Queue  # 若是multiprocessing的Queue与协程同时使用，会有问题
import requests
import time


# 任务函数
def visit_url(url_list, i):
    while url_list:
        try:
            url = url_list.pop()
            r = requests.get(url, timeout=5)
            print("【第%s个协程】响应状态码 [%s]：%s" % (i, r.status_code, url))
        except Exception as e:
            print("【第%s个协程】访问异常[%s]，原因：%s" % (i, url, e))

# 创建协程
def gevent_maker(q):
    url_list = []
    tasks = []
    i = 1
    while not q.empty():
        url_list.append(q.get()._result)  # tornado的Queue取元素的值时要用._result
        # 1个协程处理200个url，共需5个协程
        if len(url_list) == 200:
            tasks.append(gevent.spawn(visit_url, url_list, i))
            url_list = []
            i += 1
    gevent.joinall(tasks)


if __name__ == "__main__":
    q = Queue()
    with open("e:\\url.txt") as f:  # 存储了1000个url的本地文件
        for url in f:
            q.put(url.strip())  # 去掉末尾的换行符
    print("*"*20+"开始计时"+"*"*20)
    start = time.time()
    gevent_maker(q)
    end = time.time()
    print("*"*20+"结束计时"+"*"*20)
    print("总耗时：%s秒" % (end-start))