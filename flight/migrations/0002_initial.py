# Generated by Django 4.2.2 on 2023-07-02 23:34

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='companyName')),
                ('traveling_date', models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 7, 2, 23, 34, 40, 353963, tzinfo=datetime.timezone.utc))], verbose_name='travelingDate')),
                ('origin', django_countries.fields.CountryField(max_length=2)),
                ('destination', django_countries.fields.CountryField(max_length=2)),
                ('ticket_price', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(10000)], verbose_name='ticketPrice')),
                ('available_seats', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(400)], verbose_name='availableSeats')),
            ],
        ),
        migrations.CreateModel(
            name='Flight_Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_seats', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)], verbose_name='seatsNumber')),
                ('flightClass', models.CharField(choices=[('Economy', 'Economy'), ('Business', 'Business')], default='Economy', max_length=8)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=100)),
                ('payment_intent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight', to='flight.flight')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]