from django.http import JsonResponse
from .models import FinalDb
from django.shortcuts import render
from rest_framework import pagination
from .serializers import PostSerializer
from .inn import main_estimation
from rest_framework import viewsets
from haystack.query import SearchQuerySet
from rest_framework import generics, filters
from haystack.views import FacetedSearchView
from opensearchpy import OpenSearch
from opensearchpy.exceptions import OpenSearchException

client = OpenSearch(
    hosts = [{"host": "localhost", "port": 9200}],
    http_auth = ("admin", "6Wk1Cny30WOH"),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)

class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    ordering = 'row_number'

class SuppliersViewSet2(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = 'row_number'
    pagination_class = PageNumberSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'product_price', 'product_company', 'okpd2']

    def get_queryset(self):
        query = self.request.query_params.get('q', '')

        if query:
            try:
                response = client.search(
                    index="products",
                    body={
                        "query": {
                            "multi_match": {
                                "query": query,
                                "fields": ["product_name^2", "product_desc", "product_company", "inn", "ogrn", "okpd2"],
                                "fuzziness": "AUTO",  # Добавление фуззи поиска для учета опечаток
                                "prefix_length": 1,  # Минимальная длина префикса для учета фуззи поиска
                                "max_expansions": 50  # Максимальное количество вариантов для фуззи поиска
                            }
                        },
                        "size": 50  # Ограничение количества результатов
                    }
                )
                print(response)
                hits = response['hits']['hits']
                ids = [hit['_source']['row_number'] for hit in hits]  # Здесь мы используем 'row_number' вместо 'id'
                queryset = FinalDb.objects.filter(row_number__in=ids)
                return queryset
            except OpenSearchException as e:
                print(f"Ошибка OpenSearch: {e}")
                return FinalDb.objects.none()
        else:
            return FinalDb.objects.all().order_by('row_number')
    
class SuppliersViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = 'row_number'
    pagination_class = PageNumberSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'product_price', 'product_company', 'okpd2']

    def get_queryset(self):
        query = self.request.query_params.get('q', '')

        # Пример запроса с использованием OpenSearch
        response = client.search(
            index="products",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["product_name^2", "product_desc", "product_company", "inn", "ogrn", "okpd2"],
                        "fuzziness": "AUTO",  # Добавление фуззи поиска для учета опечаток
                        "prefix_length": 1,  # Минимальная длина префикса для учета фуззи поиска
                        "max_expansions": 50  # Максимальное количество вариантов для фуззи поиска
                    }
                },
                "size": 50  # Ограничение количества результатов
            }
        )
        print(response)
        hits = response['hits']['hits']
        ids = [hit['_source']['row_number'] for hit in hits]  # Здесь мы используем 'row_number' вместо 'id'
        queryset = FinalDb.objects.filter(row_number__in=ids)
        return queryset


def search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        try:
            response = client.search(
                index="products",
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["product_name^3", "product_desc^2", "product_company", "inn", "ogrn", "okpd2"]
                        }
                    },
                    "size": 50  # Получить только 50 результатов
                }
            )
            results = [hit['_source']['product_name'] for hit in response['hits']['hits']]
        except OpenSearchException as e:
            print("Ошибка OpenSearch:", e)
    suggestions = set()
    if ' ' not in query:
        for result in results:
            words = result.split()
            for word in words:
                if word.lower().startswith(query.lower()):
                    suggestions.add(word.lower())
    else:
        for result in results:
            suggestions.add(result)
    suggestions = list(suggestions)[:5]
    response_data = {
        'results': results,
        'suggestions': suggestions
    }
    print('search')
    return JsonResponse(response_data)


def okpd_search(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query:
        results = FinalDb.objects.filter(окпд2__icontains=query)
        for result in results:
            suggestions.append(result.окпд2)
        suggestions = suggestions[:5]
    return JsonResponse({'results': suggestions})

def get_recommendation(request):
    print(request)
    inn = request.GET.get('inn', '')
    agent = request.GET.get('agent', '')
    print("Received request with INN:", inn)
    print("Received request with agent:", agent)
    recommendations, rating = main_estimation(int(inn), agent)
    return JsonResponse({'recommendations': recommendations, 'rating': rating})