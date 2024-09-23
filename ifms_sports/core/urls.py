
from django.urls import path
from .views import (
    signup_view, add_team, add_player, update_match, modalidade_detail, index
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('add_team/', add_team, name='add_team'),
    path('add_player/', add_player, name='add_player'),
    path('match/update/<int:match_id>/', update_match, name='update_match'),
    path('modalidade/<str:modalidade_slug>/', modalidade_detail, name='modalidade_detail'),
]
