# Generated by Django 5.0.4 on 2024-05-23 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='promocode',
            new_name='title',
        ),
    ]
