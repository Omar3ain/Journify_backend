# Generated by Django 4.2.2 on 2023-07-03 00:31

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0004_alter_flight_traveling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='traveling_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 7, 3, 0, 31, 10, 330403, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate'),
        ),
    ]
