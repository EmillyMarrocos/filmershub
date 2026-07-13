#!/usr/bin/env python
"""
Script de gerenciamento do Django.
Comandos úteis:
  python manage.py runserver          # Rodar servidor de desenvolvimento
  python manage.py makemigrations     # Criar migrações do banco
  python manage.py migrate            # Aplicar migrações no banco
  python manage.py createsuperuser    # Criar usuário admin
  python manage.py shell              # Abrir shell do Django
  python manage.py test               # Rodar testes
"""
import os
import sys


def main():
    """Executa tarefas administrativas do Django."""
    # Define qual arquivo de configurações usar
    # Padrão: config.settings.development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. "
            "Verifique se ele está instalado e disponível no PYTHONPATH. "
            "Esqueceu de ativar o ambiente virtual?"
        ) from exc

    # Executa o comando passado no terminal
    # Ex: python manage.py runserver → execute_from_command_line(['manage.py', 'runserver'])
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
