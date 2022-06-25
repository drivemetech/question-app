from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('questions/<slug:slug>/', views.viewQuestion, name='view-Question'),
    path('question/<int:pk>/answer/', views.My_Answer.as_view(), name='answer'),
    path('question/', views.My_Question.as_view(), name='question'),
    path('register/', views.register, name='register'),
    path('notification/', views.NotificationListView.as_view(), name='notification'),
]