from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('questions/<slug:slug>/', views.viewQuestion, name='view-Question'),
    path('question/<int:pk>/answer/', views.My_Answer.as_view(), name='answer'),
    path('question/', views.My_Question.as_view(), name='question'),
    path('register/', views.register, name='register'),
    path('notification/', views.NotificationListView.as_view(), name='notification'),
    path('answer/<int:pk>/like', views.like_answer, name='like-answer'),
    path('userProfile/<slug:slug>/', views.public_profile, name='Public_Profile'),
    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            success_url='password_reset_confirm'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=' ' 
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
