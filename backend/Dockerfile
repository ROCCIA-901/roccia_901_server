FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /roccia_901

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

COPY . .
RUN mkdir -p logs
RUN chmod +x ./init.sh && chmod +x ./wait-for-it.sh
