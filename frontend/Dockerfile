FROM python
WORKDIR /frontend
COPY frontend.py /frontend
COPY requirements.txt /frontend
COPY static /frontend
COPY templates /frontend
RUN pip3 install -r requirements.txt 
EXPOSE 5000
CMD ["python3","frontend.py"]