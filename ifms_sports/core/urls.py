from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('add_team/', views.add_team, name='add_team'),
    path('add_player/', views.add_player, name='add_player'),
    path('match/update/<int:match_id>/', views.update_match, name='update_match'),
    path('modality/<str:modality_slug>/', views.modality_detail, name='modality_detail'),
    path('bracket/<slug:modality_slug>/', views.bracket_view, name='bracket'),
]
