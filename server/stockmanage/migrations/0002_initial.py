# Generated by Django 3.2.8 on 2021-11-14 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('stockmanage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercustombs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_bs', to='users.profile'),
        ),
        migrations.AddField(
            model_name='sub_account',
            name='pre_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_account', to='stockmanage.fs_account'),
        ),
        migrations.AddField(
            model_name='quarter',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quarter', to='stockmanage.year'),
        ),
        migrations.AddField(
            model_name='fs_lob',
            name='quarter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fs_lob', to='stockmanage.quarter'),
        ),
        migrations.AddField(
            model_name='fs_div',
            name='lob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fs_div', to='stockmanage.fs_lob'),
        ),
        migrations.AddField(
            model_name='fs_account',
            name='fs_div',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fs_account', to='stockmanage.fs_div'),
        ),
        migrations.AddField(
            model_name='daily_price',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stockmanage.company'),
        ),
        migrations.AddField(
            model_name='customsub_account',
            name='pre_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_account', to='stockmanage.customfs_account'),
        ),
        migrations.AddField(
            model_name='customfs_account',
            name='custom_bs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fs_account', to='stockmanage.usercustombs'),
        ),
        migrations.AddField(
            model_name='company',
            name='favorite_user',
            field=models.ManyToManyField(blank=True, related_name='favorite_company', to='users.Profile'),
        ),
    ]
