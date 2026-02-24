from django.core.management.base import BaseCommand
from micro_admin.models import User


class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_admin=True).exists():
            User.objects.create_superuser('admin', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
