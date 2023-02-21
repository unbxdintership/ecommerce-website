FROM python

WORKDIR /backend

COPY . /backend/

RUN pip install -r requirements.txt 
RUN pip list

EXPOSE 3000

CMD ["python3", "-u", "backend.py"]