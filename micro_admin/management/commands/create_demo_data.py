from django.core.management.base import BaseCommand
from micro_admin.models import User, Branch, Client, Group
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Creates demo data for client presentation'

    def handle(self, *args, **options):
        # Create Branch
        branch, _ = Branch.objects.get_or_create(
            name='Main Branch',
            defaults={
                'opening_date': date.today() - timedelta(days=365),
                'country': 'India',
                'state': 'Karnataka',
                'district': 'Bangalore',
                'city': 'Bangalore',
                'area': 'Koramangala',
                'phone_number': '9876543210',
                'pincode': '560034'
            }
        )
        self.stdout.write(f'Created branch: {branch.name}')

        # Create Staff Users
        staff_names = [
            ('john', 'John', 'Doe'),
            ('sarah', 'Sarah', 'Smith'),
            ('mike', 'Mike', 'Johnson')
        ]
        
        for username, first, last in staff_names:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': first,
                    'last_name': last,
                    'gender': 'M' if username != 'sarah' else 'F',
                    'branch': branch,
                    'user_roles': 'BranchManager',
                    'is_staff': True,
                    'is_active': True
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(f'Created staff: {username}')

        # Create Clients
        client_data = [
            ('Rajesh', 'Kumar', 'M', '9876543211'),
            ('Priya', 'Sharma', 'F', '9876543212'),
            ('Amit', 'Patel', 'M', '9876543213'),
            ('Sneha', 'Reddy', 'F', '9876543214'),
            ('Vijay', 'Singh', 'M', '9876543215'),
        ]

        for first, last, gender, phone in client_data:
            username = f'{first.lower()}{last.lower()}'
            client, created = Client.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': first,
                    'last_name': last,
                    'gender': gender,
                    'branch': branch,
                    'date_of_birth': date(1990, 1, 1) + timedelta(days=random.randint(0, 10000)),
                    'mobile': phone,
                    'country': 'India',
                    'state': 'Karnataka',
                    'district': 'Bangalore',
                    'city': 'Bangalore',
                    'area': 'Koramangala',
                    'pincode': '560034',
                    'is_active': True
                }
            )
            if created:
                client.set_password('demo123')
                client.save()
                self.stdout.write(f'Created client: {username}')

        # Create Groups
        group_names = ['Self Help Group A', 'Women Empowerment Group', 'Farmers Group']
        
        for group_name in group_names:
            group, created = Group.objects.get_or_create(
                name=group_name,
                defaults={
                    'account_number': f'GRP{random.randint(10000, 99999)}',
                    'activation_date': date.today() - timedelta(days=180),
                    'branch': branch,
                    'created_by': User.objects.filter(is_staff=True).first()
                }
            )
            if created:
                self.stdout.write(f'Created group: {group_name}')

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Staff: john / demo123, sarah / demo123, mike / demo123')
        self.stdout.write('Clients: rajeshkumar / demo123, priyasharma / demo123, etc.')
