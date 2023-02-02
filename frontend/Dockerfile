FROM python

WORKDIR /frontend

COPY frontend.py /frontend
COPY requirements.txt /frontend
COPY /static /frontend/static
COPY /templates /frontend/templates

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python","frontend.py"]