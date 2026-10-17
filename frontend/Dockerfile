FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

EXPOSE 8001

CMD ["python", "-m", "http.server", "8001", "--bind", "0.0.0.0"]
