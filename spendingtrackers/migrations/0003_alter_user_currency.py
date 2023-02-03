# Generated by Django 4.1.5 on 2023-02-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spendingtrackers', '0002_transaction_user_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(choices=[('£', '£'), ('$', '$'), ('€', '€'), ('₹', '₹'), ('¥', '¥')], default='£', max_length=1, null=True),
        ),
    ]
