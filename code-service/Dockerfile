FROM python:3.12-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ARG ENVFILE=.env.example

ENV PATH=/root/.local/bin:$PATH
ENV ENV_FILE=$ENVFILE

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/
COPY . .

EXPOSE 8001

CMD ["python", "app/code_service_main.py"]
