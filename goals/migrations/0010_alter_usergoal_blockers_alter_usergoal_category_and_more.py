# Generated by Django 4.2.2 on 2023-07-20 20:30

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rewards", "0002_userreward"),
        ("goals", "0009_alter_usergoal_friend"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usergoal",
            name="blockers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255), default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="usergoal",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_category",
                to="goals.goal",
            ),
        ),
        migrations.AlterField(
            model_name="usergoal",
            name="friend",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_friend",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="usergoal",
            name="reward",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_price",
                to="rewards.reward",
            ),
        ),
    ]
