from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.loader import render_to_string
from .models import Team, Player, Match, Modalidade
from .forms import SignUpForm
from .utils import generate_bracket_visual
import logging
from .forms import ModalidadeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import logging
import os



logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_superuser

def index(request):
    """
    Página inicial do sistema.
    """
    try:
        logger.info("Carregando a página inicial.")
        modalidades = Modalidade.objects.all()
        if not modalidades:
            logger.warning("Nenhuma modalidade encontrada.")
        else:
            logger.info(f"Modalidades carregadas: {[modalidade.nome for modalidade in modalidades]}")
        return render(request, 'core/index.html', {'modalidades': modalidades})
    except Exception as e:
        logger.error(f"Erro ao carregar a página inicial: {e}")
        return HttpResponse("Erro ao carregar a página inicial.", status=500)


@login_required
def add_player(request):
    """
    Adiciona um jogador a um time específico.
    """
    team_id = request.GET.get('team')
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        position = request.POST['position']
        team = get_object_or_404(Team, pk=request.POST['team'])
        Player.objects.create(name=name, age=age, team=team, is_if_student=True)
        logger.info(f"Jogador {name} adicionado ao time {team.name}.")
        return redirect('team_detail', pk=team.id)
    return render(request, 'core/add_player.html', {'teams': Team.objects.filter(id=team_id) if team_id else Team.objects.all()})

@login_required
def add_team(request):
    """
    Adiciona um novo time ao sistema e redireciona para adicionar jogadores.
    """
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        modalidade_id = request.POST['modalidade']
        modalidade = get_object_or_404(Modalidade, pk=modalidade_id)
        team = Team.objects.create(name=name, modalidade=modalidade, leader=request.user)
        logger.info(f"Time {name} adicionado com sucesso na modalidade {modalidade.nome}.")
        return redirect('add_player')
    return render(request, 'core/add_team.html', {'players': Player.objects.filter(team__isnull=True), 'modalidades': Modalidade.objects.all()})




@login_required
def bracket_view(request, modalidade_slug=None):
    """ 
    Exibe a visualização do chaveamento.
    """
    try:
        modalidade = get_object_or_404(Modalidade, slug=modalidade_slug)
        logger.info(f"Modalidade selecionada: {modalidade.nome}.")

        visual_path = generate_bracket_visual(modalidade)
        if visual_path and os.path.exists(os.path.join(os.getcwd(), visual_path.strip("/"))):
            return render(request, 'core/bracket.html', {'modalidade_selecionada': modalidade, 'visual_path': visual_path})
        else:
            logger.error(f"Arquivo não encontrado: {visual_path}")
            return HttpResponse("Erro ao gerar o chaveamento. Arquivo não encontrado.", status=500)
    except Exception as e:
        logger.error(f"Erro ao gerar o bracket: {e}")
        return HttpResponse("Erro ao gerar o chaveamento. Verifique os detalhes do erro no log.", status=500)

class ModalidadeListView(ListView):
    """
    Exibe a lista de todas as modalidades.
    """
    model = Modalidade
    template_name = 'core/modalidade_list.html'

def signup_view(request):
    """
    Realiza o cadastro de um novo usuário.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            logger.info(f"Novo usuário cadastrado: {username}.")
            return redirect('team_list')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def logout_view(request):
    """
    Realiza o logout do usuário e redireciona para a página de login.
    """
    logout(request)
    logger.info("Usuário desconectado.")
    return redirect('login')

@login_required 
def index_js_view(request):
    """
    Renderiza a página principal que carrega o conteúdo dinâmico do chaveamento.
    """
    logger.info("Carregando a página principal para conteúdo dinâmico.")
    return render(request, 'core/index_js.html')



@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ModalidadeListView(ListView):
    model = Modalidade
    template_name = 'core/modalidade_list.html'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ModalidadeCreateView(CreateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'core/modalidade_form.html'
    success_url = reverse_lazy('modalidade_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ModalidadeUpdateView(UpdateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'core/modalidade_form.html'
    success_url = reverse_lazy('modalidade_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class ModalidadeDeleteView(DeleteView):
    model = Modalidade
    template_name = 'core/modalidade_confirm_delete.html'
    success_url = reverse_lazy('modalidade_list')

@method_decorator(login_required, name='dispatch')
class TeamListView(ListView):
    """
    Exibe a lista de todos os times cadastrados.
    """
    model = Team
    template_name = 'core/team_list.html'

@method_decorator(login_required, name='dispatch')
class TeamDetailView(DetailView):
    """
    Exibe os detalhes de um time específico.
    """
    model = Team
    template_name = 'core/team_detail.html'

@method_decorator(login_required, name='dispatch')
class TeamCreateView(CreateView):
    """
    Cria um novo time no sistema.
    """
    model = Team
    fields = ['name', 'modalidade', 'leader']
    template_name = 'core/team_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.leader = self.request.user
        logger.info(f"Novo time criado: {form.instance.name} na modalidade {form.instance.modalidade.nome}.")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TeamUpdateView(UpdateView):
    """
    Atualiza informações de um time existente.
    """
    model = Team
    fields = ['name', 'modalidade']
    template_name = 'core/team_form.html'
    success_url = '/'

    def get_queryset(self):
        return super().get_queryset().filter(leader=self.request.user)

@method_decorator(login_required, name='dispatch')
class TeamDeleteView(DeleteView):
    """
    Exclui um time do sistema.
    """
    model = Team
    template_name = 'core/team_confirm_delete.html'
    success_url = '/'

    def get_queryset(self):
        return super().get_queryset().filter(leader=self.request.user)

@method_decorator(login_required, name='dispatch')
class MatchDetailView(DetailView):
    """
    Exibe os detalhes de um jogo específico.
    """
    model = Match
    template_name = 'core/match_detail.html'