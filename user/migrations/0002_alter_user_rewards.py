# Generated by Django 4.2.2 on 2023-07-20 20:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rewards", "0002_userreward"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="rewards",
            field=models.ManyToManyField(
                related_name="users_rewards", to="rewards.reward"
            ),
        ),
    ]