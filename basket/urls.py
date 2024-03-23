from django.urls import path
from . import views

urlpatterns = [
    path('basket_list/', views.BasketListView.as_view()),
    path('basket_detail/<int:pk>', views.BasketDetailView.as_view()),
    ]

