# Generated by Django 4.2.2 on 2023-06-24 09:39

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flight", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="flight_reservation",
            old_name="flight_id",
            new_name="flight",
        ),
        migrations.AlterField(
            model_name="flight",
            name="traveling_date",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(
                            2023, 6, 24, 9, 39, 41, 46918, tzinfo=datetime.timezone.utc
                        )
                    )
                ],
                verbose_name="travelingDate",
            ),
        ),
    ]