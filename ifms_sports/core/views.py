from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Modality, Team, Player, Match, Modality
from .forms import SignUpForm, PlayerForm, TeamForm
from .utils import generate_bracket_visual

def index(request):
    modalities = Modality.objects.all()
    if not modalities.exists():
        modalities = None
    return render(request, 'core/index.html', {'modalities': modalities})


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
            generate_bracket_visual(form.cleaned_data['modality'])
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
        
        generate_bracket_visual(match.modality)
        return redirect('index')
    return render(request, 'core/update_match.html', {'match': match})

@login_required
def modality_detail(request, modality_slug):
    modality = get_object_or_404(Modality, slug=modality_slug)
    teams = Team.objects.filter(modality=modality)
    matches = Match.objects.filter(modality=modality)
    bracket_path = generate_bracket_visual(modality)
    return render(request, 'core/modality_detail.html', {
        'modality': modality,
        'teams': teams,
        'matches': matches,
        'bracket_path': bracket_path
    })

def bracket_view(request, modality_slug):
    modality = get_object_or_404(Modality, id=modality_slug)
    return render(request, 'core/bracket.html', {'modality': modality})
