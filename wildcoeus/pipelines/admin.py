from django.contrib import admin

from . import models


admin.site.register(models.PipelineLog)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskResult)
admin.site.register(models.ValueStore)
