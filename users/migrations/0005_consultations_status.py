# Generated by Django 4.2.1 on 2023-06-21 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_consultations_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultations",
            name="status",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
