from django.db import models, connection

from app import settings

from ratestask_region.models import Regions


class Ports(models.Model):
    """
    The Ports model corresponds to the Port entity and is constructed according to the port specifications described in
    the task. However, it is not applicable to this task since the table generated by Django using this model has a
    different name compared to the original database used in the task.
    """

    code = models.TextField(primary_key=True, default='', unique=True, blank=False, null=False,
                            max_length=settings.PORT_CODE_MAX_LENGTH)
    name = models.TextField(default='', blank=False, null=False, max_length=settings.PORT_NAME_MAX_LENGTH)
    parent_slug = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='port_region')

    class Meta:
        verbose_name = 'port'
        verbose_name_plural = 'ports'

    def __str__(self):
        return f'{self.code}'

    @classmethod
    def get_ports_by_code_or_slug(cls, code_slug):
        """
        This class method return ports by making query based on their code or parent slug
        :param code: Port code
        :param slug: Parent slug
        :return: Database records
        """

        query = """
            SELECT ports.code FROM ports
            RIGHT JOIN regions
            ON regions.slug = ports.parent_slug
            WHERE regions.parent_slug = '{0}' 
                OR ports.parent_slug = '{0}' 
                OR ports.code = '{0}'
        """.format(code_slug)

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()

        return row
