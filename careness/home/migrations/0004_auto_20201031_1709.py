# Generated by Django 3.1.2 on 2020-10-31 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_auto_20201031_1648"),
    ]

    operations = [
        migrations.AddField(
            model_name="cards",
            name="name",
            field=models.CharField(default="No topic", max_length=255),
        ),
        migrations.AddField(
            model_name="subcards",
            name="name",
            field=models.CharField(default="No topic", max_length=255),
        ),
    ]
