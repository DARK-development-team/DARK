# Generated by Django 3.2.2 on 2021-05-10 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='access_key',
            field=models.IntegerField(default=3119, editable=False),
        ),
    ]
