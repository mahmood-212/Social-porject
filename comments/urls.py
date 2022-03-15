from unicodedata import name
from django.urls import path
from . import views

app_name='comments'

urlpatterns =[
    path('personalpost/<int:pk>/comment/', views.add_comment_personalpost, name='addcomment'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='remove')
]