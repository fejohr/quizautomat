FROM python:3.8.8-slim
EXPOSE 80
WORKDIR /root
COPY templates /root/templates
COPY main.py /root/main.py
COPY quizuser.py /root/quizuser.py
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt
CMD python main.py
