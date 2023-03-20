from django.db import models

from app import settings


class Regions(models.Model):
    """
    Regions model represents the Region entity
    This class is defined based on what specified about the region inside the task descriptions.
    Overall, it does not have application in this task because the table that is created by django based on this entity
    has different name in comparison to the initial database from the task.
    """
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
