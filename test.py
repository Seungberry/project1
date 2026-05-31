import time
import threading
import requests

def stress_test_task(thread_id):
    print(f"线程 {thread_id} 开始发送请求...")
    try:
        start = time.time()
        # 增加超时设置，防止脚本无限死等
        res = requests.post(
            "http://127.0.0.1:5000/api/chat/send", 
            json={"question": "试用期没签合同怎么办？"},
            timeout=30 
        )
        end = time.time()
        print(f"线程 {thread_id} | 响应耗时: {end - start:.2f}s, 状态码: {res.status_code}")
        if res.status_code == 200:
            print(f"线程 {thread_id} 结果: {res.json().get('answer')[:20]}...")
    except Exception as e:
        print(f"线程 {thread_id} 发生错误: {e}")

# 模拟10个用户同时咨询
threads = []
for i in range(10):
    t = threading.Thread(target=stress_test_task, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程结束
for t in threads:
    t.join()
print("所有压力测试任务已完成")