from django.apps import AppConfig


class DarkModelsConfig(AppConfig):
    name = 'dark.models'

    def ready(self):
        from .tournament import Tournament, TournamentRound
        from dark.models.tournament.team import Team, TeamRole, TeamMember, TeamBot

        from django.contrib import admin

        admin.site.register(Tournament)
        admin.site.register(TournamentRound)
        admin.site.register(Team)
        admin.site.register(TeamRole)
        admin.site.register(TeamMember)
        admin.site.register(TeamBot)


default_app_config = 'dark.models.DarkModelsConfig'
