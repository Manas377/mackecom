# Generated by Django 3.0.5 on 2020-04-29 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_ordereditem_qty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordereditem',
            old_name='title',
            new_name='item',
        ),
    ]
