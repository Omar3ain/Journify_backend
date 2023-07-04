# Generated by Django 4.2.2 on 2023-07-04 01:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hotelReservation", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stayreservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("confirmed", "Confirmed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=100,
            ),
        ),
    ]
