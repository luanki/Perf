#!/bin/bash

# 获取传入的 TCP 端口
TCP_PORT=$1

# 在这里可以使用 TCP_PORT 进行任何需要的操作
# 例如，将 TCP_PORT 作为参数传递给 startup.py

python3 mobileperf/android/startup.py "$TCP_PORT"
