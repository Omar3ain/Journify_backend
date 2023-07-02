# Generated by Django 4.2.1 on 2023-07-02 05:16

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0006_alter_flight_traveling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='traveling_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 7, 2, 5, 16, 56, 618362, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate'),
        ),
    ]
