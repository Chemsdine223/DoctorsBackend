# Generated by Django 4.2.1 on 2023-06-19 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultations",
            name="heure_de_consultation",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="consultations",
            name="date_de_consultation",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
