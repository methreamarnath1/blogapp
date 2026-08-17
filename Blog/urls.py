from django.urls import path
from Blog import views

urlpatterns = [
    path('', views.home_view, name='home_url'),
    path('blog_create_page/', views.blog_create_view, name='blog_create_url'),
    path('blog_detail/<int:id>/', views.blog_detail_view, name='blog_detail_url'),
    path('login/', views.login_view, name='login_url'),
    path('signup/', views.signup_view, name='signup_url'),
    path('logout/', views.logout_view, name='logout_url'),
    path('profile/', views.profile_view, name='profile_url'),
    path('profile/reset-password/', views.reset_password_view, name='reset_password_url'),
    path('deleteblog/<int:id>', views.blog_delete_view, name='deleteblog'),
    path('edit/<int:id>/', views.edit_view, name='edit_blog_url'),
    path('edit_page/<int:id>/', views.edit_page_view, name='editpage'),
]