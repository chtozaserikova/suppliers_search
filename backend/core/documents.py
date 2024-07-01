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
                "filter": {
                    "russian_synonym_filter": {
                        "type": "synonym",
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "russian_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "russian_synonym_filter",
                            "russian_stemmer",
                            "snowball"
                        ]
                    }
                }
            }
        }
    class Django:
        model = FinalDb
        fields = {
            "product_name": fields.TextField(analyzer="russian_analyzer"),
            "product_desc": fields.TextField(analyzer="russian_analyzer"),
            "product_price": fields.KeywordField(),
            "product_company": fields.TextField(analyzer="russian_analyzer"),
            "inn": fields.KeywordField(),
            "ogrn": fields.KeywordField(),
            "okpd2": fields.KeywordField(),
            "row_number": fields.IntegerField(),  
        }
