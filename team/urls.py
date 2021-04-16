from django.urls import path
from team.views import *

urlpatterns = [
    path('create', create_team_view, name="Create Team"),
    path('<int:teamid>', show_team_info_view, name="Show Team Info"),
    path('<int:teamid>/remove', remove_team_view, name="Remove Team"),
    path('<int:teamid>/change_name', change_team_name_view, name="Change Team Name"),
    path('<int:teamid>/manage_roles', manage_team_roles_view, name="Manage Team Roles"),
    path('<int:teamid>/add_role', add_team_role_view, name="Add Team Role"),
    path('<int:teamid>/<int:roleid>/modify_role', modify_role_view, name="Modify Team Role"),
    path('<int:teamid>/<int:roleid>/remove_role', remove_role_view, name="Remove Team Role"),
    path('<int:teamid>/add_member', add_team_member_view, name="Add Team Member"),
    path('<int:teamid>/<int:teammemberid>/remove_member', remove_team_member_view, name="Remove Team Member"),
    path('<int:teamid>/<int:teammemberid>', show_team_member_info_view, name="Show Team Member Info"),
    path('<int:teamid>/<int:teammemberid>/change_role', change_team_member_role_view, name="Change Team Member Role"),
]
