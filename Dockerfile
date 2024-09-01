# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements 文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制 Django 项目文件
COPY . .

# 启动 Django 应用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
