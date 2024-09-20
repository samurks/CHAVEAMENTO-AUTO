
from django.urls import path
from .views import (
    signup_view, add_player, add_team, bracket_view, index_js_view,
    TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView, 
    TeamDeleteView, MatchDetailView, ModalidadeListView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index_js_view, name='index'),
    path('bracket/<str:modalidade_slug>/', bracket_view, name='modalidade_bracket'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('team/new/', TeamCreateView.as_view(), name='team_new'),
    path('team/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    path('match/<int:pk>/', MatchDetailView.as_view(), name='match_detail'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_player/', add_player, name='add_player'),
    path('add_team/', add_team, name='add_team'),
    path('modalidades/', ModalidadeListView.as_view(), name='modalidades'),
]
