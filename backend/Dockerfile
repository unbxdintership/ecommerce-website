FROM python

WORKDIR /backend

COPY db_init.py /backend
COPY requirements.txt /backend
COPY db_initialise.py /backend
COPY db_operations.py /backend
COPY redis_initialise.py /backend
COPY redis_operation.py /backend
COPY backend.py /backend
COPY config.ini /backend

RUN pip install -r requirements.txt 
RUN pip list

EXPOSE 3000

CMD ["python3","backend.py"]