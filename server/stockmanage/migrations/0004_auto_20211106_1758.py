# Generated by Django 3.2.8 on 2021-11-06 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stockmanage', '0003_auto_20211028_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFS_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(blank=True, help_text='계정명', max_length=255, null=True)),
                ('account_amount', models.FloatField(blank=True, help_text='계정명에 대한 자산', null=True)),
                ('coef', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCustomBS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_title', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_code', models.CharField(blank=True, max_length=100, null=True)),
                ('bs_year', models.IntegerField(blank=True, help_text='사업연도', null=True)),
                ('qt_name', models.CharField(blank=True, help_text='1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011', max_length=30, null=True)),
                ('lob', models.CharField(blank=True, help_text='연결(CFS)/일반(OFS)', max_length=30, null=True)),
                ('sj_div', models.CharField(blank=True, help_text='재무제표구분(BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)', max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_bs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomSUB_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(blank=True, help_text='계정명', max_length=255, null=True)),
                ('account_amount', models.FloatField(blank=True, help_text='계정명에 대한 금액', null=True)),
                ('coef', models.IntegerField(blank=True, default=1, null=True)),
                ('pre_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_account', to='stockmanage.customfs_account')),
            ],
        ),
        migrations.AddField(
            model_name='customfs_account',
            name='custom_bs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fs_account', to='stockmanage.usercustombs'),
        ),
    ]