# Generated by Django 4.2.2 on 2023-06-30 14:07

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0009_alter_flight_traveling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='traveling_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 6, 30, 14, 7, 36, 523748, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate'),
        ),
    ]
