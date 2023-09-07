# Dockerfile 指令
# 基于 基础镜像
FROM python:3.6.10

# 将构建环境下的文件OR目录, 复制到镜像中的/code目录下, 
ADD . /app

# 设置/切换 当前工作目录 为 /code
WORKDIR /app

# 假设run.py是项目启动入口, 
# ENTRYPOINT 和 CMD 指令均可用于指定容器启动时要运行的命令, 
# 区别在于 CMD 命令可以被 docker run命令覆盖
ENTRYPOINT ["python", "main.py"]
CMD ["python", "main.py"]
