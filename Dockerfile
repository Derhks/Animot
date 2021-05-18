FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
