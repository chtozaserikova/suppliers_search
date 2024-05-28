from rest_framework import serializers
from .models import FinalDb

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalDb
        fields = ("row_number", "product_name", "product_desc", "product_price", "product_company", "inn", "ogrn", "okpd2")
        lookup_field = 'row_number'
        extra_kwargs = {
            'url': {'lookup_field': 'row_number'}
        }
