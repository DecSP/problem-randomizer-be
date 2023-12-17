# Generated by Django 4.2.7 on 2023-12-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("problems", "0003_alter_problem_source_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="content",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="problem",
            name="sample_test_data",
            field=models.JSONField(default=dict),
        ),
    ]