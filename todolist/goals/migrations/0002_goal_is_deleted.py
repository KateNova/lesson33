# Generated by Django 4.1.3 on 2022-12-04 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалена'),
        ),
    ]