from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify 

class Modality(models.Model):
    nome = models.CharField(_("Name"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super(Modality, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = _("Modalidade")
        verbose_name_plural = _("Modalidades")

class Player(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    age = models.IntegerField(_("Age"))
    is_leader = models.BooleanField(_("Is leader"), default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Jogador")
        verbose_name_plural = _("Jogadores")

class Team(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    leader = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Leader"))
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE, verbose_name=_("Modality"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Times")

class Match(models.Model):
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE, default=1, verbose_name=_("Modality"))
    team_a = models.ForeignKey(Team, related_name='team_a', on_delete=models.CASCADE, verbose_name=_("Team A"))
    team_b = models.ForeignKey(Team, related_name='team_b', on_delete=models.CASCADE, verbose_name=_("Team B"))
    score_a = models.IntegerField(_("Score A"), default=0)
    score_b = models.IntegerField(_("Score B"), default=0)
    date = models.DateTimeField(_("Date"))
    completed = models.BooleanField(_("Completed"), default=False)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Winner"))

    def save(self, *args, **kwargs):
        if self.score_a != self.score_b:
            self.winner = self.team_a if self.score_a > self.score_b else self.team_b
        else:
            self.winner = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"

    class Meta:
        verbose_name = _("Partida")
        verbose_name_plural = _("Partidas")
