from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuppliersViewSet, SuppliersViewSet2, search, okpd_search, get_recommendation

router = DefaultRouter()
router.register('suppliers', SuppliersViewSet, basename='suppliers')
router.register('suppliers2', SuppliersViewSet2, basename='suppliers2')

urlpatterns = [
    path('search/', search, name='search'),
    path('okpd_search/', okpd_search, name='okpd_search'), 
    path('get_recommendation/', get_recommendation, name='get_recommendation'),
    # path('inn/<int:inn>/<str:agent>/', get_inn_recommendations, name='get_inn_recommendations'),
    # path('category-recommendations/', category_recommendations_view, name='category_recommendations'),

    path("", include(router.urls))
]
