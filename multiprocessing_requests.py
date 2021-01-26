from multiprocessing import Process, Queue
import requests
import time


# 任务函数
def visit_url(q, i):
    while not q.empty():
        try:
            url = q.get_nowait()
            r = requests.get(url, timeout=5)
            print("【第%s个子进程】响应状态码 [%s]：%s" % (i, r.status_code, url))
        except Exception as e:
            print("【第%s个子进程】访问异常[%s]，原因：%s" % (i, url, e))


if __name__ == "__main__":
    q = Queue()
    with open("e:\\url.txt") as f:  # 存储了1000个url的本地文件
        for url in f:
            q.put(url.strip())  # 去掉末尾换行符等
    print("*"*20+"开始计时"+"*"*20)
    start = time.time()
    p_list = []
    # 创建5个子进程
    for i in range(5):
        p = Process(target=visit_url, args=(q, i+1))
        p_list.append(p)
        p.start()
        print(p)
    # 等待所有子进程执行完成
    for p in p_list:
        p.join()
        print(p)
    end = time.time()
    print("*"*20+"结束计时"+"*"*20)
    print("总耗时：%s秒" % (end-start))