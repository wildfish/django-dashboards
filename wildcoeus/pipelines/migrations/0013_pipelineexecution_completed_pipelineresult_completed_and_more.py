# Generated by Django 4.1.3 on 2023-01-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pipelines", "0012_remove_taskresult_pipeline_task_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipelineexecution",
            name="completed",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="pipelineresult",
            name="completed",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="taskexecution",
            name="completed",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="taskexecution",
            name="started",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="pipelineexecution",
            name="started",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="pipelineresult",
            name="started",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="taskresult",
            name="completed",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="taskresult",
            name="started",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
