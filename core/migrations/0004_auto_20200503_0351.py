# Generated by Django 3.0.5 on 2020-05-03 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200503_0307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordereditem',
            old_name='ordered',
            new_name='is_ordered',
        ),
    ]