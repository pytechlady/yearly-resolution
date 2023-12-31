# Generated by Django 4.2.2 on 2023-06-22 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goals", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Friend",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("friend_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="usergoal",
            name="friend",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_goals",
                to="goals.friend",
            ),
        ),
    ]
