from django.contrib import admin

from demo.demo_app import models


admin.site.register(models.FlatText)
admin.site.register(models.Vehicle)
admin.site.register(models.Parameter)
admin.site.register(models.Data)
