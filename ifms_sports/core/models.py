from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Gere um novo slug com base no nome se o slug não existir ou se o nome mudar
        if not self.slug or self.slug != slugify(self.nome):
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.OneToOneField(User, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_if_student = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    sport = models.CharField(max_length=50)
    team_a = models.ForeignKey(Team, related_name='team_a', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='team_b', on_delete=models.CASCADE)
    score_a = models.IntegerField(default=0)
    score_b = models.IntegerField(default=0)
    date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"
