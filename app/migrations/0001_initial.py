# Generated by Django 5.1.6 on 2025-04-13 18:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('referral_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('submit_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='LoanCalculation',
            fields=[
                ('loancalculation_id', models.AutoField(primary_key=True, serialize=False)),
                ('expected_grad_date', models.DateTimeField()),
                ('submit_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SharedEmail',
            fields=[
                ('sharedemail_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('submit_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='IndividualLoan',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_num', models.IntegerField()),
                ('principal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest', models.DecimalField(decimal_places=2, max_digits=5)),
                ('loan_type', models.CharField(max_length=50)),
                ('sem_received', models.CharField(max_length=100)),
                ('loancalculation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.loancalculation')),
            ],
        ),
    ]
