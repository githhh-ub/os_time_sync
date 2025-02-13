#!/usr/bin/env python3
import sys
import os
import subprocess
import platform
from typing import List, Tuple

class EnvironmentChecker:
    def __init__(self):
        self.required_packages = {
            'ntplib': 'ntplib',
            'python': 'python3'
        }
        self.os_specific_commands = {
            'windows': {
                'package_manager': 'pip',
                'admin_check': self._check_windows_admin,
                'install_python': 'https://www.python.org/downloads/',
                'run_as_admin': 'powershell -Command Start-Process python.exe -Verb RunAs'
            },
            'linux': {
                'package_manager': 'pip3',
                'admin_check': self._check_linux_root,
                'install_python': 'apt-get update && apt-get install python3-pip',
                'run_as_admin': 'sudo '
            },
            'darwin': {
                'package_manager': 'pip3',
                'admin_check': self._check_macos_admin,
                'install_python': 'brew install python',
                'run_as_admin': 'sudo '
            }
        }

    def _check_windows_admin(self) -> bool:
        """检查Windows是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _check_linux_root(self) -> bool:
        """检查Linux是否以root用户运行"""
        return os.getuid() == 0

    def _check_macos_admin(self) -> bool:
        """检查MacOS是否有管理员权限"""
        return os.getuid() == 0

    def check_environment(self) -> Tuple[bool, List[str]]:
        """检查Python环境和ntplib模块是否安装"""
        missing_packages = []
        
        # 检查Python版本
        python_version = sys.version_info
        if python_version.major != 3:
            missing_packages.append('Python 3.x')
        
        # 检查ntplib模块
        try:
            __import__('ntplib')
        except ImportError:
            missing_packages.append('ntplib')
        
        return len(missing_packages) == 0, missing_packages

    def install_package(self, package_name: str) -> bool:
        """安装指定包"""
        os_type = platform.system().lower()
        if os_type not in self.os_specific_commands:
            print(f"不支持的操作系统: {platform.system()}")
            return False

        commands = self.os_specific_commands[os_type]
        installer = commands['package_manager']
        
        try:
            print(f"\n正在安装 {package_name}...")
            if os_type == 'windows':
                subprocess.check_call([installer, 'install', package_name])
            else:
                subprocess.check_call([installer, 'install', '--user', package_name])
            return True
        except subprocess.CalledProcessError as e:
            print(f"安装 {package_name} 失败: {str(e)}")
            return False

    def run_main_script(self):
        """运行主时间同步脚本"""
        from time_sync import main
        main()

def main():
    checker = EnvironmentChecker()
    
    print("\n=== 环境检查 ===")
    env_ok, missing = checker.check_environment()
    
    if not env_ok:
        print("\n未找到以下必需组件:")
        for pkg in missing:
            print(f"- {pkg}")
        
        choice = input("\n是否允许自动下载并安装缺失的组件？(y/n): ").strip().lower()
        if choice != 'y':
            print("请手动安装后重试。")
            return
            
        for pkg in missing:
            if pkg == 'Python 3.x':
                os_type = platform.system().lower()
                if os_type == 'windows':
                    print("\n请访问以下链接下载并安装Python 3.x:")
                    print(checker.os_specific_commands[os_type]['install_python'])
                    return
                elif os_type in checker.os_specific_commands:
                    print(f"\n正在安装Python 3.x...")
                    subprocess.check_call(checker.os_specific_commands[os_type]['install_python'], shell=True)
                return
                
            if pkg == 'ntplib':
                if not checker.install_package('ntplib'):
                    print("\n请使用管理员权限重新运行此脚本。")
                    return
    
    # 环境检查通过，运行主程序
    checker.run_main_script()

if __name__ == '__main__':
    main()