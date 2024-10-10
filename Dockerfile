# 使用 Python 3.9-slim 作为基础镜像
FROM python:3.9-slim

# 更新包管理器并安装必备工具
RUN apt-get update && apt-get install -y \
    usbutils \
    android-tools-adb \
    openjdk-17-jre-headless

# 设置工作目录
WORKDIR /app

# 将当前目录中的所有内容复制到容器中
COPY . /app

# 安装 Python 依赖（如有）
RUN pip install -r requirements.txt

# 运行脚本
CMD ["python3", "adbconnect.py"]