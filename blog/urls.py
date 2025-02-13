from django.urls import path
from . import views
 
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('category/<slug:slug>/', views.category_list, name="category_list"),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('comment/add/<int:post_id>', views.comment_form, name='comment_form'),
]
