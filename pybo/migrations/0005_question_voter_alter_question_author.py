# Generated by Django 4.2.16 on 2025-03-25 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pybo", "0004_answer_modify_date_question_modify_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="voter",
            field=models.ManyToManyField(
                related_name="voter_question", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_question",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
