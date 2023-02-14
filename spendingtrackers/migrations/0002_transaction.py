# Generated by Django 4.1.3 on 2023-02-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spendingtrackers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expenditure', models.BooleanField()),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paid', models.DateTimeField(blank=True, null=True)),
                ('time_paid', models.TimeField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Groceries', 'Groceries'), ('Salary', 'Salary'), ('Bills', 'Bills'), ('Rent', 'Rent'), ('Gym', 'Gym'), ('Restaurant', 'Restaurant'), ('Vacation', 'Vacation'), ('Travel', 'Travel'), ('Gift', 'Gift'), ('Investments', 'Investments'), ('Savings', 'Savings'), ('Entertainment', 'Entertainment'), ('Internet', 'Internet'), ('Healthcare', 'Healthcare'), ('Lifestyle', 'Lifestyle'), ('Insurance', 'Insurance'), ('Other', 'Other')], max_length=50)),
            ],
        ),
    ]
