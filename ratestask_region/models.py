from django.db import models

from app import settings


class Regions(models.Model):
    slug = models.TextField(primary_key=True, default='', unique=True, blank=False, null=False,
                            max_length=settings.REGION_SLUG_MAX_LENGTH)
    name = models.TextField(default='', blank=False, null=False, max_length=settings.REGION_NAME_MAX_LENGTH)
    parent_slug = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='region_parent')

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'

    def __str__(self):
        return f'{self.slug}'
