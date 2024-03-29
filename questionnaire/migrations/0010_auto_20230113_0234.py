# Generated by Django 3.2.4 on 2023-01-12 18:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_auto_20230113_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accumulated_prize', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='input_cost',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(100)]),
        ),
    ]
