# admin_setup.py
import os
import sys
from django.core.management import call_command

def setup_django():
    """Garante que o Django esteja configurado."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()

def create_superuser_interactive():
    """Inicia o processo interativo de criação de superusuário."""
    setup_django()
    
    print("="*50)
    print(" Assistente de Criação de Superusuário")
    print("="*50)
    print("\nPor favor, siga as instruções abaixo.")
    
    # Chama o comando interativo do Django
    call_command('createsuperuser')
    
    print("\nProcesso finalizado.")
    input("Pressione Enter para fechar esta janela.")