from django.urls import path
from .views import (
  CosmeticListView,
  CosmeticDetailView,
  cosmetic_search_item
)

app_name = 'cosmetics'

urlpatterns = [
    path("", CosmeticListView.as_view(), name="cosmetic-list"),
    path("cosmetic-detail/<slug>/", CosmeticDetailView.as_view(), name="cosmetic-detail"),
    path("cosmetic-search-item/", cosmetic_search_item, name="cosmetic-search-item"),
]