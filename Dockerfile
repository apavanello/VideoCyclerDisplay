FROM python:3.11-slim as builder


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput


FROM python:3.11-slim

WORKDIR /app

RUN addgroup --system django-user && adduser --system --group django-user
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app .
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app/media && \
    chown -R django-user:django-user /app
USER django-user
EXPOSE 8000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "core.wsgi:application"]