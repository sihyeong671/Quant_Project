# Generated by Django 3.2 on 2021-07-31 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DBmanageapp', '0002_alter_fs_account_fs_div'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fs_lob',
            old_name='exits',
            new_name='exist',
        ),
    ]