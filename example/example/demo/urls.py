from django.urls import path

from . import views

app_name = 'demo'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='index'),
    path('custom/', views.ItemCustomListView.as_view(), name='custom-1'),

    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
]
