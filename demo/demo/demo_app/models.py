from django.db import models


class FlatText(models.Model):
    slug = models.SlugField()
    text = models.TextField()

    def __str__(self):
        return self.slug
