# Generated migration to populate LoanRepaymentEvery table

from django.db import migrations


def populate_loan_repayment_every(apps, schema_editor):
    LoanRepaymentEvery = apps.get_model('micro_admin', 'LoanRepaymentEvery')
    for i in range(1, 6):
        LoanRepaymentEvery.objects.get_or_create(value=i)


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0019_auto_20160915_0759'),
    ]

    operations = [
        migrations.RunPython(populate_loan_repayment_every),
    ]
