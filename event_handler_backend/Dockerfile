FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --chown=appuser:appuser . .

ENV JWT_ALGORITHM="HS256"
ENV JWT_EXPIREY=604800
ENV DEBUG=0
ENV DJANGO_ALLOWED_HOSTS=localhost

USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_handler_backend.wsgi:application"]
