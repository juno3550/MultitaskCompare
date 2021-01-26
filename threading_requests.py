from threading import Thread
import queue
import requests
import time


# 任务函数
def visit_url(q, i):
    while not q.empty():
        try:
            url = q.get()
            r = requests.get(url, timeout=5)
            print("【第%s个子线程】响应状态码 [%s]：%s" % (i, r.status_code, url))
        except Exception as e:
            print("【第%s个子线程】访问异常[%s]，原因：%s" % (i, url, e))


if __name__ == "__main__":
    q = queue.Queue()
    with open("e:\\url.txt") as f:  # 存储了1000个url的本地文件
        for url in f:
            q.put(url.strip())  # 去掉末尾换行符等
    print("*"*20+"开始计时"+"*"*20)
    start = time.time()
    t_list = []
    # 创建5个子线程
    for i in range(5):
        t = Thread(target=visit_url, args=(q, i+1))
        t_list.append(t)
        t.start()
        print(t)
    # 等待所有子线程执行完成
    for t in t_list:
        t.join()
        print(t)
    end = time.time()
    print("*"*20+"结束计时"+"*"*20)
    print("总耗时：%s秒" % (end-start))