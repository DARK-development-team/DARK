# Generated by Django 3.2.2 on 2021-05-10 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_alter_tournament_access_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='access_key',
            field=models.IntegerField(default=6807, editable=False),
        ),
    ]
