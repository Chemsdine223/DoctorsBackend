# Generated by Django 4.2.1 on 2023-06-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_schedule_dimanche_alter_schedule_jeudi_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultations",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]