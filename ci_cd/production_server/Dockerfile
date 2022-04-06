FROM python:3.9-buster
ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./app.py","--host=0.0.0.0"]
