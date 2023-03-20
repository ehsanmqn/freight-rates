from django.db import models, connection

from ratestask_port.models import Ports


class Prices(models.Model):
    """
    The price entity is represented by the Prices model, which has been constructed according to the task description
    specifications. However, it is not applicable to this task since the table generated by Django using this model has a
    different name compared to the original database used in the task.
    """
    orig_code = models.ForeignKey(Ports, on_delete=models.CASCADE, null=True, blank=True, related_name='ports_origin')
    dest_code = models.ForeignKey(Ports, on_delete=models.CASCADE, null=True, blank=True, related_name='ports_destin')
    day = models.DateField()
    price = models.IntegerField()

    class Meta:
        verbose_name = 'price'
        verbose_name_plural = 'prices'

    def __str__(self):
        return f'{self.price}'

    @classmethod
    def get_avg_daily_prices_v1(cls, origins, destins, date_from, date_to):
        """
        This class methode queries for average daily prices by giving dates, origins, and destinations.
        :param origins: Origin ports code
        :param destins: Destination ports code
        :param date_from: Date from in YYY-MM-DD format
        :param date_to: Date to in YYY-MM-DD format
        :return: List of data
        """

        with connection.cursor() as cursor:
            cursor.execute("SELECT DATE(dates.day) AS day, "
                           "CASE "
                           "WHEN COUNT(prices.price) >= 3 THEN COALESCE(AVG(prices.price), NULL) "
                           "END AS average_price "
                           "FROM (SELECT generate_series(%s::date, %s::date, '1 day') AS day) AS dates "
                           "LEFT JOIN prices ON prices.orig_code IN %s "
                           "AND prices.dest_code IN %s "
                           "AND DATE(prices.day) = dates.day "
                           "WHERE dates.day BETWEEN %s::date AND %s::date "
                           "GROUP BY dates.day ", [date_from, date_to,
                                                   origins, destins,
                                                   date_from, date_to])
            rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        return data

    @classmethod
    def get_avg_daily_prices_v2(cls, origins, destins, date_from, date_to):
        """
        This class methode queries for average daily prices by giving dates, origins, and destinations. This function
        contains full date sequence between the given dates.
        :param origins: Origin port code or parent slug
        :param destins: Destination port code or parent slug
        :param date_from: Date from in YYY-MM-DD format
        :param date_to: Date to in YYY-MM-DD format
        :return: List of data
        """

        query = """
                WITH 
                  origin_codes AS (
                    SELECT code FROM ports WHERE code IN ('{}') OR parent_slug IN ('{}')
                  ),
                  dest_codes AS (
                    SELECT code FROM ports WHERE code IN ('{}') OR parent_slug IN ('{}')
                  )
                SELECT DATE(dates.day) AS day, 
                CASE 
                    WHEN COUNT(prices.price) >= 3 THEN COALESCE(AVG(prices.price), NULL)
                END AS average_price
                FROM (SELECT generate_series('{}'::date, '{}'::date, '1 day') AS day) AS dates
                LEFT JOIN prices ON prices.orig_code IN (SELECT code FROM origin_codes)
                AND prices.dest_code IN (SELECT code FROM dest_codes)
                AND DATE(prices.day) = dates.day
                WHERE dates.day BETWEEN '{}'::date AND '{}'::date
                GROUP BY dates.day;
            """.format(origins, origins, destins, destins, date_from, date_to, date_from, date_to)

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        return data
