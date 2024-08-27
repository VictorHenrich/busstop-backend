FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt update -y && apt install git -y

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "run_migrate.py",  "&&",  "python3", "src/run_api.py"]