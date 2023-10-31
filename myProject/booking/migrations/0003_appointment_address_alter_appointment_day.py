# Generated by Django 4.2.6 on 2023-10-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_staff_remove_appointment_time_ordered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='address',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='day',
            field=models.CharField(choices=[('2023-10-28', '2023-10-28'), ('2023-10-29', '2023-10-29'), ('2023-10-30', '2023-10-30'), ('2023-10-31', '2023-10-31'), ('2023-11-01', '2023-11-01'), ('2023-11-02', '2023-11-02'), ('2023-11-03', '2023-11-03')], default='Monday', max_length=50),
        ),
    ]