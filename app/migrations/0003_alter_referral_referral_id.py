# Generated by Django 5.1.6 on 2025-04-06 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_referral_referral_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='referral_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
