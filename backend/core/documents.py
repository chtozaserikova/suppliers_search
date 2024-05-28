from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from .models import FinalDb

@registry.register_document
class SuppliersDocument(Document):

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "standard"
                    },
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stop", "snowball"]
                    }
                }
            }
        }

    class Django:
        model = FinalDb
        fields = {
            "product_name": fields.TextField(analyzer="custom_analyzer"),
            "product_desc": fields.TextField(analyzer="custom_analyzer"),
            "product_price": fields.TextField(analyzer="custom_analyzer"),
            "product_company": fields.TextField(analyzer="custom_analyzer"),
            "inn": fields.KeywordField(),
            "ogrn": fields.KeywordField(),
            "okpd2": fields.KeywordField(),
            "row_number": fields.IntegerField(),  
        }
