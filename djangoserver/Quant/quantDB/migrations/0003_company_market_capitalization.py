# Generated by Django 3.2 on 2021-05-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantDB', '0002_auto_20210525_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='market_capitalization',
            field=models.IntegerField(blank=True, help_text='시가총액', null=True),
        ),
    ]
