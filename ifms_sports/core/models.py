from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.OneToOneField(User, on_delete=models.CASCADE)
    sport = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

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
