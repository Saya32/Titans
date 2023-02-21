# Generated by Django 4.1.3 on 2023-02-21 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spendingtrackers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_choices',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='category_fk',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spendingtrackers.category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receipt',
            field=models.ImageField(blank=True, default=1, upload_to='receipt_images'),
            preserve_default=False,
        ),
    ]
