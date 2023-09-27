FROM python:3.6.10

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "main.py"]
