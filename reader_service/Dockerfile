FROM python:3

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./run.py /run.py
COPY ./run.sh /run.sh

CMD ["sh", "run.sh"]
