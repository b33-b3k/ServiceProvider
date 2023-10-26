# Generated by Django 4.2.6 on 2023-10-26 06:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_alter_appointment_id_alter_staff_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='id',
        ),
        migrations.AddField(
            model_name='staff',
            name='staff_id',
            field=models.AutoField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
