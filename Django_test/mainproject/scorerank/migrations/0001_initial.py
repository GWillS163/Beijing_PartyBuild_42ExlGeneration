# Generated by Django 3.2.3 on 2021-05-27 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=10)),
                ('score', models.FloatField(max_length=10)),
                ('rank', models.FloatField(max_length=10)),
            ],
        ),
    ]
