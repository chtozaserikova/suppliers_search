from django.db import models



class FinalDb(models.Model):
    row_number = models.IntegerField(primary_key=True)
    product_name = models.TextField(blank=True, null=True)
    product_desc = models.TextField(blank=True, null=True)
    product_price = models.TextField(blank=True, null=True)
    product_company = models.TextField(blank=True, null=True)
    inn = models.BigIntegerField(blank=True, null=True)
    ogrn = models.BigIntegerField(blank=True, null=True)
    okpd2 = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'products'

