#!/bin/bash

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "警告：建议不要以root身份运行此脚本"
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "未检测到Python 3.x环境，请先安装"
    exit 1
fi

# 安装ntplib（如果尚未安装）
pip3 list | grep ntplib > /dev/null || pip3 install --user ntplib

# 运行主程序
python3 start_sync.py

echo "按任意键退出..."
read -n 1