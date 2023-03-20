from django.db import models

from ratestask_port.models import Ports


class Prices(models.Model):
    orig_code = models.ForeignKey(Ports, on_delete=models.CASCADE, null=True, blank=True, related_name='ports_origin')
    dest_code = models.ForeignKey(Ports, on_delete=models.CASCADE, null=True, blank=True, related_name='ports_destin')
    day = models.DateField()
    price = models.IntegerField()

    class Meta:
        verbose_name = 'price'
        verbose_name_plural = 'prices'

    def __str__(self):
        return f'{self.price}'