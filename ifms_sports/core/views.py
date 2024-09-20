from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Team, Player, Match  
from .forms import SignUpForm  
from .utils import generate_bracket


def index(request):
    return render(request, 'core/index.html')

def add_player(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        position = request.POST['position']
        team_id = request.POST['team']
        team = get_object_or_404(Team, pk=team_id)
        Player.objects.create(name=name, age=age, team=team, is_if_student=True)
        return redirect('team_detail', pk=team.id)
    return render(request, 'core/add_player.html', {'teams': Team.objects.all()})

def add_team(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        player_ids = request.POST.getlist('players')
        team = Team.objects.create(name=name, sport="Futebol", leader=request.user)  # Exemplo: esporte fixo
        for player_id in player_ids:
            player = get_object_or_404(Player, pk=player_id)
            player.team = team
            player.save()
        return redirect('team_list')
    return render(request, 'core/add_team.html', {'players': Player.objects.filter(team__isnull=True)})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

class TeamListView(ListView):
    model = Team
    template_name = 'core/team_list.html'

class MatchDetailView(DetailView):
    model = Match
    template_name = 'core/match_detail.html'

@login_required
def bracket_view(request):
    bracket = generate_bracket()
    return render(request, 'core/bracket.html', {'bracket': bracket})

@method_decorator(login_required, name='dispatch')
class TeamDetailView(DetailView):
    model = Team
    template_name = 'core/team_detail.html'

@method_decorator(login_required, name='dispatch')
class TeamCreateView(CreateView):
    model = Team
    fields = ['name', 'sport', 'leader']
    template_name = 'core/team_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.leader = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TeamUpdateView(UpdateView):
    model = Team
    fields = ['name', 'sport']
    template_name = 'core/team_form.html'
    success_url = '/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(leader=self.request.user)

@method_decorator(login_required, name='dispatch')
class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'core/team_confirm_delete.html'
    success_url = '/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(leader=self.request.user)

# Função de notificação
def notify_user(user_email, subject, message):
    send_mail(
        subject,
        message,
        'admin@ifms.com',
        [user_email],
    )
