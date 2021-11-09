# Generated by Django 3.2.8 on 2021-11-09 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_favorite_company'),
        ('stockmanage', '0004_auto_20211106_1758'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercustombs',
            options={'verbose_name': 'Custom BS', 'verbose_name_plural': 'Custom BS'},
        ),
        migrations.AddField(
            model_name='company',
            name='favorite_user',
            field=models.ManyToManyField(blank=True, related_name='favorite_company', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='usercustombs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_bs', to='users.profile'),
        ),
    ]
