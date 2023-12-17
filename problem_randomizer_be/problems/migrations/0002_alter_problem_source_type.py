# Generated by Django 4.2.7 on 2023-12-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("problems", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="problem",
            name="source_type",
            field=models.CharField(choices=[("cf", "Codeforces"), ("ac", "AtCoder"), ("cs", "CSES")], max_length=2),
        ),
    ]