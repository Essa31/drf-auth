from django.urls import path

from .views import GameListView, GameDetailView, PostListView, PostDetailView

urlpatterns = [
    path('', GameListView.as_view(), name='games_list'),
    path('<int:pk>/', GameDetailView.as_view(), name='games_detail'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]