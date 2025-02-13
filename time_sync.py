import ntplib
from time import ctime
import sys

def get_ntp_time():
    """
    从微软NTP服务器获取当前时间
    """
    try:
        # 创建NTP客户端实例
        ntp_client = ntplib.NTPClient()
        
        # 使用微软的NTP服务器
        response = ntp_client.request('time.windows.com', version=3)
        
        # 将NTP时间转换为Unix时间戳
        current_time = response.tx_time
        
        return current_time
    
    except Exception as e:
        print(f"获取NTP时间失败: {str(e)}")
        return None

def sync_system_time(ntp_time):
    """
    同步系统时间
    """
    try:
        # Windows系统使用命令行设置时间
        if sys.platform.startswith('win'):
            import subprocess
            command = f'wmic os set datetime={ctime(ntp_time)}'
            subprocess.run(command, shell=True, check=True)
            
        # Linux/Mac系统使用date命令设置时间
        elif sys.platform.startswith(('linux', 'darwin')):
            import subprocess
            command = ['sudo', 'date', '-s', '@%d' % int(ntp_time)]
            subprocess.run(command, check=True)
            
        print("系统时间已成功更新！")
        return True
        
    except Exception as e:
        print(f"设置系统时间失败: {str(e)}")
        return False

def main():
    """
    主程序入口
    """
    print("开始获取网络时间...")
    
    # 获取NTP时间
    ntp_time = get_ntp_time()
    if ntp_time is None:
        return
    
    # 显示当前NTP时间
    print(f"网络时间: {ctime(ntp_time)}")
    
    # 同步系统时间
    if sync_system_time(ntp_time):
        print(f"新的系统时间: {ctime(ntp_time)}")

if __name__ == "__main__":
    main()