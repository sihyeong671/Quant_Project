# Generated by Django 3.2.8 on 2021-11-14 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_name', models.CharField(blank=True, max_length=100, null=True)),
                ('corp_name_eng', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_name', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_code', models.CharField(blank=True, max_length=100, null=True)),
                ('ceo_name', models.CharField(blank=True, max_length=100, null=True)),
                ('corp_cls', models.CharField(blank=True, max_length=100, null=True)),
                ('jurir_no', models.CharField(blank=True, max_length=100, null=True)),
                ('bizr_no', models.CharField(blank=True, max_length=100, null=True)),
                ('adres', models.CharField(blank=True, max_length=100, null=True)),
                ('hm_url', models.CharField(blank=True, max_length=100, null=True)),
                ('ir_url', models.CharField(blank=True, max_length=100, null=True)),
                ('phn_no', models.CharField(blank=True, max_length=100, null=True)),
                ('fax_no', models.CharField(blank=True, max_length=100, null=True)),
                ('induty_code', models.CharField(blank=True, max_length=100, null=True)),
                ('est_dt', models.CharField(blank=True, max_length=100, null=True)),
                ('acc_mt', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': '기업',
                'verbose_name_plural': '기업',
                'ordering': ['corp_name'],
            },
        ),
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
            name='CustomSUB_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(blank=True, help_text='계정명', max_length=255, null=True)),
                ('account_amount', models.FloatField(blank=True, help_text='계정명에 대한 금액', null=True)),
                ('coef', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('market_cap', models.FloatField(blank=True, help_text='시가총액', null=True)),
                ('open', models.FloatField(blank=True, help_text='시가', null=True)),
                ('high', models.FloatField(blank=True, help_text='고가', null=True)),
                ('low', models.FloatField(blank=True, help_text='저가', null=True)),
                ('close', models.FloatField(blank=True, help_text='종가', null=True)),
                ('volume', models.FloatField(blank=True, help_text='거래량', null=True)),
            ],
            options={
                'verbose_name': '주가',
                'verbose_name_plural': '주가',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Dart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dart_code', models.CharField(blank=True, help_text='고유번호', max_length=10, null=True)),
                ('company_name_dart', models.CharField(blank=True, help_text='회사명', max_length=50, null=True)),
                ('short_code', models.CharField(blank=True, help_text='종목코드', max_length=30, null=True)),
                ('recent_modify', models.CharField(blank=True, help_text='최종변경일자', max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'dart info',
                'verbose_name_plural': 'dart info',
            },
        ),
        migrations.CreateModel(
            name='FS_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(blank=True, help_text='계정명', max_length=255, null=True)),
                ('account_amount', models.FloatField(blank=True, help_text='계정명에 대한 자산', null=True)),
                ('account_add_amount', models.FloatField(blank=True, help_text='계정명에 대한 누적 금액', null=True)),
                ('account_detail', models.CharField(blank=True, help_text='계정상세', max_length=255, null=True)),
            ],
            options={
                'verbose_name': '계정명',
                'verbose_name_plural': '계정명',
                'ordering': ['account_name'],
            },
        ),
        migrations.CreateModel(
            name='FS_Div',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sj_div', models.CharField(blank=True, help_text='재무제표구분(BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)', max_length=255, null=True)),
            ],
            options={
                'verbose_name': '재무제표구분',
                'verbose_name_plural': '재무제표구분',
            },
        ),
        migrations.CreateModel(
            name='FS_LoB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lob', models.CharField(blank=True, help_text='연결(CFS)/일반(OFS)', max_length=30, null=True)),
                ('exist', models.IntegerField(blank=True, default=0, null=True)),
                ('unit', models.CharField(blank=True, max_length=30, null=True)),
                ('ROA', models.FloatField(blank=True, null=True)),
                ('ROE', models.FloatField(blank=True, null=True)),
                ('GPA', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '연결/일반',
                'verbose_name_plural': '연결/일반',
            },
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qt_name', models.CharField(blank=True, help_text='1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011', max_length=30, null=True)),
            ],
            options={
                'verbose_name': '분기별 데이터',
                'verbose_name_plural': '분기별 데이터',
            },
        ),
        migrations.CreateModel(
            name='SUB_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(blank=True, help_text='계정명', max_length=255, null=True)),
                ('account_amount', models.FloatField(blank=True, help_text='계정명에 대한 금액', null=True)),
                ('account_add_amount', models.FloatField(blank=True, help_text='계정명에 대한 누적 금액', null=True)),
                ('account_detail', models.CharField(blank=True, help_text='계정상세', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'sub계정명',
                'verbose_name_plural': 'sub계정명',
            },
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
            ],
            options={
                'verbose_name': 'Custom BS',
                'verbose_name_plural': 'Custom BS',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bs_year', models.IntegerField(blank=True, help_text='사업연도', null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='year', to='stockmanage.company')),
            ],
            options={
                'verbose_name': '연도별 데이터',
                'verbose_name_plural': '연도별 데이터',
                'ordering': ['bs_year'],
            },
        ),
    ]
