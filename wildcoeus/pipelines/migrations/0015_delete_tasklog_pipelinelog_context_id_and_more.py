# Generated by Django 4.1.3 on 2023-01-19 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pipelines", "0014_remove_pipelineresult_input_data_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TaskLog",
        ),
        migrations.AddField(
            model_name="pipelinelog",
            name="context_id",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="pipelinelog",
            name="context_type",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]