# Generated by Django 2.2.5 on 2020-09-13 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'pending'), (1, 'playing'), (2, 'finished')], default=0),
        ),
    ]
