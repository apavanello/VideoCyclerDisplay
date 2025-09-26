# create_admin.py
import os
import sys

# Configura o ambiente Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

# Verifica se um superusuário já existe
if User.objects.filter(is_superuser=True).exists():
    print("Um superusuário já existe. Nenhuma ação foi tomada.")
    input("Pressione Enter para sair.")
else:
    print("Nenhum superusuário encontrado. Por favor, crie um agora.")
    # Chama o comando 'createsuperuser' de forma interativa
    call_command('createsuperuser')
    print("\nSuperusuário criado com sucesso!")
    input("Pressione Enter para sair.")