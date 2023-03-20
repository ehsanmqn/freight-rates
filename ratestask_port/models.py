from django.db import models

from app import settings

from ratestask_region.models import Regions


class Ports(models.Model):
    code = models.TextField(primary_key=True, default='', unique=True, blank=False, null=False,
                            max_length=settings.PORT_CODE_MAX_LENGTH)
    name = models.TextField(default='', blank=False, null=False, max_length=settings.PORT_NAME_MAX_LENGTH)
    parent_slug = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='port_region')

    class Meta:
        verbose_name = 'port'
        verbose_name_plural = 'ports'

    def __str__(self):
        return f'{self.code}'
