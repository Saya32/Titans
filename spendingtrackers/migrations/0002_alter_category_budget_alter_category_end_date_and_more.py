# Generated by Django 4.1.3 on 2023-02-15 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spendingtrackers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='spending_limit',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]