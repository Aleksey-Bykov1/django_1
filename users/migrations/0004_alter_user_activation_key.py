# Generated by Django 3.2.6 on 2021-09-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key',
            field=models.CharField(blank=True, default=18, max_length=128),
        ),
    ]
