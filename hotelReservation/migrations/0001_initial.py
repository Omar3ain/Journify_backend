# Generated by Django 4.2.2 on 2023-06-29 12:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StayReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('numberOfRooms', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('numberOfPeople', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('startDate', models.DateField(auto_now_add=True)),
                ('numberOfDays', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=2, default=20, max_digits=7)),
                ('room_type', models.CharField(blank=True, choices=[('S', 'Single'), ('D', 'Double')], max_length=1, null=True)),
                ('hotel', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
