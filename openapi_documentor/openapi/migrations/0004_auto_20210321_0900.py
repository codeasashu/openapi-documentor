# Generated by Django 3.1.7 on 2021-03-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openapi', '0003_auto_20210321_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]