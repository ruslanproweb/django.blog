from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchResults.as_view(), name='search'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('categories/<int:category_id>/', views.category_articles, name='category_articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),

    path('login/', views.login_view, name='login'),
    path('registration/', views.register_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('articles/create/', views.create_article_view, name='create'),
    path('articles/<int:pk>/update/', views.UpdateArticleView.as_view(), name='update'),
    path('articles/<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete'),

    path('<str:obj_type>/<int:obj_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('author/<str:username>', views.author_articles, name='author_articles'),
]