# Generated by Django 4.2.2 on 2023-07-02 23:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0002_initial'),
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='hotelName')),
                ('description', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='hotelDescription')),
                ('city', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='city')),
                ('image', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='hotelImage')),
                ('room_price', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(7000)], verbose_name='roomPrice')),
                ('available_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='availableRooms')),
                ('longitude', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='longitude')),
                ('latitude', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='latitude')),
                ('avg_rating', models.FloatField(default=0)),
                ('countryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.country')),
            ],
        ),
    ]