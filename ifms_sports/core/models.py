# core/models.py

from django.db import models
from django.contrib.auth.models import User

class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nome

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    is_leader = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, default=1)
    team_a = models.ForeignKey(Team, related_name='team_a', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='team_b', on_delete=models.CASCADE)
    score_a = models.IntegerField(default=0)
    score_b = models.IntegerField(default=0)
    date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Determinar o vencedor com base no placar
        if self.score_a != self.score_b:
            self.winner = self.team_a if self.score_a > self.score_b else self.team_b
        else:
            self.winner = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"
