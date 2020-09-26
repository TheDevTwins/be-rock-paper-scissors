# Generated by Django 2.2.5 on 2020-09-26 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='player',
            name='pick',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rock'), (1, 'paper'), (2, 'scissors')], null=True),
        ),
    ]