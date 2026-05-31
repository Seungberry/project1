import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

def plot_performance():
    models = ['GLM-4-Flash (单并发)', 'GLM-4-Flash (10并发)']
    
    # 模拟测试的真实平均值（约87.21s）
    # 模拟对比：单次调用约1.5s vs 10个并发时的平均耗时
    avg_response_time = [1.5, 87.21] 

    # 成功率统计：10个请求的状态码均为200，成功率为100%
    success_rate = [100, 100]

    plt.figure(figsize=(10, 5))
    
    # 1. 响应耗时对比（体现高并发下的延迟）
    plt.subplot(1, 2, 1)
    plt.bar(models, avg_response_time, color=['#165DFF', '#FF7D00']) 
    plt.title('并发压力对响应耗时的影响')
    plt.ylabel('平均响应秒数')

    # 2. 并发稳定性测试
    plt.subplot(1, 2, 2)
    plt.bar(models, success_rate, color='#00B42A')
    plt.title('接口请求成功率')
    plt.ylabel('百分比 (%)')
    plt.ylim(0, 110)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_performance()