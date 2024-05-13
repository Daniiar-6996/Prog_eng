from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # path('', views.HomeListView.as_view(), name='home'),
    path('detail/', views.HomeDetailView.as_view(), name='detail_page'),
    path('edit-page', views.edit_page, name='edit_page'),
    path('update-page/<int:id>', views.update_page, name='update_page'),
    path('delete-page/<int:id>', views.delete_page, name='delete_page'),
    path ('login', views.MyprojectLoginView.as_view(), name='login_page'),
    path ('register', views.RegisterUserView.as_view(), name='register_page'),
    path ('logout', views.MyProjectLogout.as_view(), name='logout_page'),
    path('result/', views.home, name='result'),  # Добавляем новый URL-шаблон для обработки результатов анализа
    path('', views.home, name='home'),

]
