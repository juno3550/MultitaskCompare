from gevent import monkey; monkey.patch_all()
import gevent
from tornado.queues import Queue
import requests
import time
from multiprocessing import Process


# 任务函数
def visit_url(args):
        try:
            r = requests.get(args.split(" ")[0], timeout=5)
            print("【第%s个子进程的第%s个协程】响应状态码 [%s]：%s" % (args.split(" ")[1], args.split(" ")[2], r.status_code, args.split(" ")[0]))
        except Exception as e:
            print("【第%s个子进程的第%s个协程】访问异常[%s]，原因：%s" % (args.split(" ")[1], args.split(" ")[2], args.split(" ")[0], e))

# 创建协程
def gevent_maker(q, p_i):
    url_list = []
    c_i = 1
    while not q.empty():
        url_list.append(q.get()._result)
        # 每个进程存满200个url后，则创建200个协程来访问url
        if len(url_list) == 200:
            tasks = []
            for url in url_list:
                # 由于传值需要是字符串，故使用join()拼接所需实参
                tasks.append(gevent.spawn(visit_url, " ".join([url, str(p_i), str(c_i)])))
                c_i += 1
            gevent.joinall(tasks)
    return


if __name__ == "__main__":
    q = Queue()
    with open("e:\\url.txt") as f:  # 存储了1000个url的本地文件
        for url in f:
            q.put(url.strip())  # 去掉末尾的换行符
    print("*"*20+"开始计时"+"*"*20)
    start = time.time()
    p_list = []
    # 创建5个子进程
    for i in range(5):
        p = Process(target=gevent_maker, args=(q, i+1))
        p_list.append(p)
        p.start()
        print(p)
    for p in p_list:
        p.join()
        print(p)
    end = time.time()
    print("*"*20+"结束计时"+"*"*20)
    print("总耗时：%s秒" % (end-start))