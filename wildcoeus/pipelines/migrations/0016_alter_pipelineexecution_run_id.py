# Generated by Django 4.1.3 on 2023-02-09 14:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("pipelines", "0015_delete_tasklog_pipelinelog_context_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pipelineexecution",
            name="run_id",
            field=models.CharField(default=uuid.uuid4, max_length=255),
        ),
    ]
