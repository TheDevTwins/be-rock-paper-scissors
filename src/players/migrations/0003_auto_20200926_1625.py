# Generated by Django 2.2.5 on 2020-09-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_auto_20200926_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='player',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(0, 'in_game'), (1, 'lost'), (2, 'won')], default=0),
        ),
    ]
