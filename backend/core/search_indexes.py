from haystack import indexes
from .models import FinalDb

class SuppliersWithIdsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    product_name = indexes.CharField(model_attr='product_name')
    product_price = indexes.CharField(model_attr='product_price', null=True)
    product_desc = indexes.CharField(model_attr='product_desc', null=True)
    product_company = indexes.CharField(model_attr='product_company', null=True)
    inn = indexes.CharField(model_attr='inn', null=True)
    ogrn = indexes.CharField(model_attr='ogrn', null=True)
    okpd2 = indexes.CharField(model_attr='okpd2', null=True)

    def get_model(self):
        return FinalDb

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

