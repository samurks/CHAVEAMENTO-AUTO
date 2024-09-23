from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Team, Player, Match, Modality

@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    search_fields = ('nome',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'is_leader', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('is_leader',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'modality', 'created_at')
    search_fields = ('name', 'leader__name')
    list_filter = ('modality',)
    fieldsets = (
        (_('General Info'), {'fields': ('name', 'leader', 'modality')}),
    )

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('modality', 'team_a', 'team_b', 'score_a', 'score_b', 'date', 'completed', 'winner')
    search_fields = ('team_a__name', 'team_b__name', 'winner__name')
    list_filter = ('modality', 'completed')
