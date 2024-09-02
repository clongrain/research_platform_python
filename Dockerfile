# 使用官方 Python 3.11 镜像作为基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 将项目文件复制到容器中
COPY . .

# 安装项目依赖并清理缓存
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn \
    && rm -rf /root/.cache

# 暴露项目端口
EXPOSE 8000

# 设置启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Django.wsgi:application"]
