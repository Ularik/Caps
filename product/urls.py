from django.urls import path
from . import views

urlpatterns = [
    path('product_list/', views.StorageListView.as_view()),
    path('index/', views.IndexListView.as_view()),
    path('product_discounts/', views.ProductDiscountView.as_view()),
    path('product_bestsellers/', views.ProductBestsellersListView.as_view()),
    path('product_favorites/', views.FavoriteListView.as_view()),
    path('product_detail/<int:pk>/', views.ProductDetailView.as_view()),
    path('product_for_basket/<int:pk>/', views.ProductForBasketView.as_view()),
    path('product_create/', views.StorageCreateView.as_view()),
    path('product_update/<int:pk>/', views.StorageUpdateView.as_view()),
    path('product_delete/<int:pk>/', views.StorageDeleteView.as_view())
]
