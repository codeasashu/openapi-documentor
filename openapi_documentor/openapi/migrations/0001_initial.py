# Generated by Django 3.1.7 on 2021-03-21 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Openapi doc', max_length=200)),
                ('doc', models.TextField(blank=True)),
                ('rev', models.CharField(default='1.0.0', max_length=20)),
                ('version', models.CharField(choices=[('3.0.0', '3.0.0'), ('3.0.1', '3.0.1'), ('3.0.2', '3.0.2')], default='3.0.0', max_length=20)),
                ('created', models.DateTimeField(verbose_name='date published')),
                ('modified', models.DateTimeField(verbose_name='date modified')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
