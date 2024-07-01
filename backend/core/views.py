from django.http import JsonResponse
from .models import FinalDb
from django.shortcuts import render
from rest_framework import pagination
from rest_framework.response import Response
from .serializers import PostSerializer
from .inn import assign_supplier_category, get_inn_reccomends
from rest_framework import viewsets
from rest_framework import generics, filters
from opensearchpy import OpenSearch
from django.db.models import Q

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

    def get_queryset(self):
        queryset = FinalDb.objects.all().order_by('row_number')
        цена = self.request.query_params.get('price', None)
        поставщик = self.request.query_params.get('supplier', None)
        объем = self.request.query_params.get('volume', None)
        окпд2 = self.request.query_params.get('okpd', None)
        название = self.request.query_params.get('name', None)
        инн = self.request.query_params.get('inn', None)
        огрн = self.request.query_params.get('ogrn', None)

        if цена:
            try:
                price_value = float(цена)
                queryset = queryset.filter(product_price__lt=price_value)
            except ValueError:
                pass
        if поставщик:
            queryset = queryset.filter(product_company__icontains=поставщик)
        if объем:
            queryset = queryset.filter(product_desc__icontains=объем)
        if окпд2:
            queryset = queryset.filter(okpd2__icontains=окпд2)
        if название:
            queryset = queryset.filter(product_name__icontains=название)
        if инн:
            queryset = queryset.filter(inn__icontains=инн)
        if огрн:
            queryset = queryset.filter(ogrn__icontains=огрн)

        return queryset

    
class SuppliersViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = 'row_number'
    pagination_class = PageNumberSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_name", "product_desc", "product_company", "inn", "ogrn", "okpd2"]

    def get_queryset(self):
        print("SuppliersViewSet call")  
        queryset = FinalDb.objects.all().order_by('row_number') 
        query = self.request.query_params.get('search', '')
        print("Received query parameter:", query)  # Печать значения параметра q

        if query:  # Проверка, что запрос не пустой
            # Пример запроса с использованием OpenSearch
            response = client.search(
                index="products",
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["product_name", "product_desc", "product_company", "inn", "ogrn", "okpd2"],
                            "fuzziness": "AUTO",  # Добавление фуззи поиска для учета опечаток
                            "prefix_length": 1, # Минимальная длина префикса для учета фуззи поиска
                            "max_expansions": 50  # Максимальное количество вариантов для фуззи поиска
                        }
                    },
                    "size": 50  # Ограничение количества результатов
                }
            )
            hits = response['hits']['hits']
            ids = [int(hit['_id']) for hit in hits]
            print(ids)
            queryset = FinalDb.objects.filter(row_number__in=ids).order_by('row_number')
            print("Queryset count after filtering:", queryset.count())
            
            self.queryset = queryset
            return queryset
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print("Serialized data (paginated):", serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print("Serialized data:", serializer.data)
        return Response(serializer.data)


def get_queryset(self):
    """
    Optionally restricts the returned suppliers, by filtering against
    a `q` query parameter in the URL.
    """
    print("get_queryset call")  
    queryset = FinalDb.objects.all().order_by('row_number')
    query = self.request.query_params.get('q', None)
    if query:
        queryset = queryset.filter(Q(product_name__icontains=query))
    return queryset

def search(request):
    print("search call")  
    query = request.GET.get('q', '').strip()
    suggestions = set()

    # Если строка запроса не пуста
    if query:
        # Если запрос не содержит пробелов
        if ' ' not in query:
            results = FinalDb.objects.filter(product_name__istartswith=query)
            for result in results:
                words = result.product_name.split()
                for word in words:
                    if word.lower().startswith(query.lower()):
                        suggestions.add(word.lower())

        # Если запрос заканчивается на пробел
        elif ' ' in query:
            results = FinalDb.objects.filter(product_name__icontains=query)
            for result in results:
                suggestions.add(result.product_name)

        # Предоставляем только первые 5 предложений
        suggestions = list(suggestions)[:5]

    return JsonResponse({'results': suggestions})

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
    recommendations, rating = get_inn_reccomends(int(inn), agent)
    print(recommendations)
    category = assign_supplier_category(recommendations)
    return JsonResponse({'recommendations': recommendations, 'rating': rating, 'category':category})