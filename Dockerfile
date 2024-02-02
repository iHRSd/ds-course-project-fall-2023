FROM python:3.8.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generator-update.py .

CMD ["python", "generator-update.py"]
EXPOSE 5000
