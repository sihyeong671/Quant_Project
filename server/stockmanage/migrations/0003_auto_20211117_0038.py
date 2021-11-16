# Generated by Django 3.2.8 on 2021-11-16 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanage', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_price',
            name='cfs_pbr',
            field=models.FloatField(blank=True, help_text='PBR', null=True),
        ),
        migrations.AddField(
            model_name='daily_price',
            name='cfs_per',
            field=models.FloatField(blank=True, help_text='PER', null=True),
        ),
        migrations.AddField(
            model_name='daily_price',
            name='ofs_pbr',
            field=models.FloatField(blank=True, help_text='PBR', null=True),
        ),
        migrations.AddField(
            model_name='daily_price',
            name='ofs_per',
            field=models.FloatField(blank=True, help_text='PER', null=True),
        ),
        migrations.AddField(
            model_name='fs_lob',
            name='net_income',
            field=models.FloatField(blank=True, help_text='당기순이익(CIS)', null=True),
        ),
        migrations.AddField(
            model_name='fs_lob',
            name='total_capital',
            field=models.FloatField(blank=True, help_text='자본총계(BS)', null=True),
        ),
    ]
