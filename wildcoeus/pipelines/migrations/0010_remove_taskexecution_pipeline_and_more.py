# Generated by Django 4.1.3 on 2023-01-17 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pipelines", "0009_remove_pipelineresult_pipeline_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskexecution",
            name="pipeline",
        ),
        migrations.RemoveField(
            model_name="taskexecution",
            name="started",
        ),
        migrations.RemoveField(
            model_name="taskresult",
            name="config",
        ),
        migrations.RemoveField(
            model_name="taskresult",
            name="input_data",
        ),
        migrations.AddField(
            model_name="pipelineexecution",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "PENDING"),
                    ("RUNNING", "RUNNING"),
                    ("DONE", "DONE"),
                    ("CONFIG_ERROR", "CONFIG_ERROR"),
                    ("VALIDATION_ERROR", "VALIDATION_ERROR"),
                    ("RUNTIME_ERROR", "RUNTIME_ERROR"),
                    ("CANCELLED", "CANCELLED"),
                ],
                default="PENDING",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="taskexecution",
            name="pipeline_result",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="task_executions",
                to="pipelines.pipelineresult",
            ),
        ),
        migrations.AddField(
            model_name="taskexecution",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "PENDING"),
                    ("RUNNING", "RUNNING"),
                    ("DONE", "DONE"),
                    ("CONFIG_ERROR", "CONFIG_ERROR"),
                    ("VALIDATION_ERROR", "VALIDATION_ERROR"),
                    ("RUNTIME_ERROR", "RUNTIME_ERROR"),
                    ("CANCELLED", "CANCELLED"),
                ],
                default="PENDING",
                max_length=255,
            ),
        ),
    ]
