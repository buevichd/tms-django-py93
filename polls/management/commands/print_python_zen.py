from django.core.management import BaseCommand


# Важно! Название класса должно быть именно Command
class Command(BaseCommand):
    # Текст, который будет выведен при вызове
    # python3 manage.py print_python_zen --help
    help = 'Prints python zen'

    # Главный метод, который работает при вызове
    # python3 manage.py print_python_zen --help
    def handle(self, *args, **options):
        import this