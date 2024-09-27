from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Modality, Team, Player, Match, Modality
from .forms import SignUpForm, PlayerForm, TeamForm


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

