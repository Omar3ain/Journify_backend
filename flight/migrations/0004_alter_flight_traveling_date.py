# Generated by Django 4.2 on 2023-07-03 01:17

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0003_alter_flight_traveling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='traveling_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 7, 3, 1, 17, 57, 514550, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate'),
        ),
    ]
