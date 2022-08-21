from django.urls import path

from .views import BikeListView, BikeDetailView, PostListView, PostDetailView

urlpatterns = [
    path('', BikeListView.as_view(), name='bike_list'),
    path('<int:pk>/', BikeDetailView.as_view(), name='bike_detail'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]