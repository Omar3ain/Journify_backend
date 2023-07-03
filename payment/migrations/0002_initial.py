# Generated by Django 4.2.2 on 2023-07-02 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '0002_initial'),
        ('hotelReservation', '0002_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(default=False)),
                ('flightResId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flight.flight_reservation')),
                ('stayResId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotelReservation.stayreservation')),
            ],
        ),
    ]