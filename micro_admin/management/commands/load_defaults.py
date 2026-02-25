from django.core.management.base import BaseCommand
from micro_admin.models import LoanRepaymentEvery


class Command(BaseCommand):
    help = 'Creates Loan Repayment Every'

    def handle(self, *args, **options):
        # Clear existing values to ensure fresh data
        count_before = LoanRepaymentEvery.objects.count()
        self.stdout.write(f'Found {count_before} existing LoanRepaymentEvery records')
        
        for i in range(1, 6):
            obj, created = LoanRepaymentEvery.objects.get_or_create(value=i)
            if created:
                self.stdout.write(f'Created LoanRepaymentEvery with value={i}')
            else:
                self.stdout.write(f'LoanRepaymentEvery with value={i} already exists')
        
        count_after = LoanRepaymentEvery.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully ensured Loan Repayment Every values. Total records: {count_after}'))
