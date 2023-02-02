FROM python

WORKDIR /backend
# RUN pip install --ungrade pip
COPY requirements.txt /backend
COPY db_initialise.py /backend
COPY db_operations.py /backend
COPY redis_initialise.py /backend
COPY redis_operation.py /backend
COPY backend.py /backend
COPY config.ini /backend
RUN pip install -r requirements.txt 
# RUN pip list
EXPOSE 3000
#/Users/unbxd/Desktop/ecommerce-website/backend
#RUN  python3 db_initialise.py
CMD ["python3","backend.py"]