# Generated by Django 4.1.3 on 2022-11-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_account_delete_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="username",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
