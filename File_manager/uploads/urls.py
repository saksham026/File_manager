from django.urls import path
from .views import (
    FileListView,
    FileDetailView,
    FileCreateView,
    FileUpdateView,
    FileDeleteView,
    UserFileListView
)
from . import views

urlpatterns = [
    path('', FileListView.as_view(), name='file-home'),
    path('user/<str:username>', UserFileListView.as_view(), name='user-files'),
    path('post/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('post/new/', FileCreateView.as_view(), name='file-create'),
    path('post/<int:pk>/update/', FileUpdateView.as_view(), name='file-update'),
    path('post/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),
    path('media/Files/<int:pk>',FileDeleteView.as_view(),name='file-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='file-about'),
]
