from django.urls import path
from . import views

urlpatterns = [
    path('basket_list/', views.BasketListView.as_view()),
    path('basket_detail/<int:pk>/', views.BasketDetailView.as_view()),
    path('basket_delete/<int:pk>/', views.BasketDeleteView.as_view())
    ]

