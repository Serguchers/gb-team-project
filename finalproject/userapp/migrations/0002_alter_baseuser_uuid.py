# Generated by Django 3.2 on 2022-07-13 22:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a507aec8-19e5-4bcb-bcbc-b0d76e5fe636'), primary_key=True, serialize=False),
        ),
    ]
