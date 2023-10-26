# Generated by Django 4.2.6 on 2023-10-26 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_remove_inquiry_timestamp_staff_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='staff',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='staff',
            name='experience',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='rating',
            field=models.FloatField(default='3'),
        ),
    ]