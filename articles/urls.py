from django.urls import path, include
from . import views

app_name = 'articles'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('create_article/', views.CreateArticleView.as_view(), name='create-article'),

    path('article/<str:author>/<slug:slug>/', include([
        path('edit_article/', views.UpdateArticleView.as_view(), name='edit-article'),
        path('delete/', views.DeleteArticleView.as_view(), name='delete-article'),
        path('add_comment/', views.add_comment, name='add-comment'),
        path('', views.ArticleDetailsView.as_view(), name='details'),
        
    ])),

    path('article/like_article/', views.like_article, name='like-article'),
    path('article/like_comment', views.like_comment, name='like-comment'),
]   