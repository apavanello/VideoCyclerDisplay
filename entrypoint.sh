#!/bin/sh

# Encerra o script se qualquer comando falhar
set -e

# Garante que o usuário 'django-user' seja o dono das pastas de volume.
# Isso é executado como 'root' antes da aplicação iniciar.
echo "Checking volume permissions..."
chown -R django-user:django-user /app/media
chown -R django-user:django-user /app/db

# Executa as migrações do banco de dados
# O 'gosu' executa o comando como o usuário 'django-user'
echo "Applying database migrations..."
python manage.py migrate --noinput

# Inicia a aplicação principal como 'django-user'
# "$@" passa o CMD do Dockerfile para o gosu
echo "Starting application..."
exec "$@"