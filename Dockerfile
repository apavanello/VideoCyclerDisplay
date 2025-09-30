# --- Builder Stage (sem alterações) ---
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

# --- Final Stage ---
FROM python:3.11-slim
WORKDIR /app

# Instala 'gosu' para troca de usuário segura e cria o usuário
RUN apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*
RUN addgroup --system django-user && adduser --system --group django-user

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app .
ENV PATH="/opt/venv/bin:$PATH"

# Copia o script de entrypoint e o torna executável
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["entrypoint.sh"]

# Expõe a porta e define o comando padrão a ser executado pelo entrypoint
USER django-user
EXPOSE 8000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "core.wsgi:application"]