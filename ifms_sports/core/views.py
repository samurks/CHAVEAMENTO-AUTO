# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Modalidade, Team, Player, Match
from .forms import SignUpForm, PlayerForm, TeamForm
from .utils import generate_bracket_visual

def index(request):
    modalidades = Modalidade.objects.all()
    return render(request, 'core/index.html', {'modalidades': modalidades})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PlayerForm()
    return render(request, 'core/add_player.html', {'form': form})

@login_required
def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            generate_bracket_visual(form.cleaned_data['modalidade'])
            return redirect('index')
    else:
        form = TeamForm()
    return render(request, 'core/add_team.html', {'form': form})

@login_required
def update_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        match.score_a = request.POST['score_a']
        match.score_b = request.POST['score_b']
        match.completed = True
        match.save()
        
        # Atualizar o bracket após registrar o resultado de uma partida
        generate_bracket_visual(match.modalidade)
        return redirect('index')
    return render(request, 'core/update_match.html', {'match': match})

@login_required
def modalidade_detail(request, modalidade_slug):
    modalidade = get_object_or_404(Modalidade, slug=modalidade_slug)
    teams = Team.objects.filter(modalidade=modalidade)
    matches = Match.objects.filter(modalidade=modalidade)
    bracket_path = generate_bracket_visual(modalidade)
    return render(request, 'core/modality_detail.html', {
        'modalidade': modalidade,
        'teams': teams,
        'matches': matches,
        'bracket_path': bracket_path
    })
