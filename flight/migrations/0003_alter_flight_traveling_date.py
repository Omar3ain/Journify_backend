# Generated by Django 4.2 on 2023-06-24 15:14

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_alter_flight_traveling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='traveling_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 6, 24, 15, 14, 54, 889687, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate'),
        ),
    ]
